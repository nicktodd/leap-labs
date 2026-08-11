package com.neueda.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.Statement;

// The fix: settlement_id is a natural key. UPSERT (INSERT ... ON CONFLICT)
// means running this loader any number of times against the same CSV
// converges on the same result - never duplicates.
public class IdempotentLoader {

    static final String URL = "jdbc:postgresql://localhost:5434/sprint7";
    static final String USER = "postgres";
    static final String PASSWORD = "leappass";

    public static void main(String[] args) throws Exception {
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            try (Statement st = conn.createStatement()) {
                st.execute("""
                    CREATE TABLE IF NOT EXISTS settled_trades (
                        settlement_id VARCHAR(20) PRIMARY KEY,
                        account_id VARCHAR(20),
                        ticker VARCHAR(20),
                        quantity NUMERIC,
                        settled_date DATE
                    )
                    """);
            }

            String upsertSql = """
                INSERT INTO settled_trades
                    (settlement_id, account_id, ticker, quantity, settled_date)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (settlement_id) DO UPDATE SET
                    account_id = EXCLUDED.account_id,
                    ticker = EXCLUDED.ticker,
                    quantity = EXCLUDED.quantity,
                    settled_date = EXCLUDED.settled_date
                """;

            int processed = 0;
            try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/settlements.csv"));
                 PreparedStatement ps = conn.prepareStatement(upsertSql)) {
                br.readLine(); // header
                String line;
                while ((line = br.readLine()) != null) {
                    String[] cols = line.split(",");
                    ps.setString(1, cols[0]);
                    ps.setString(2, cols[1]);
                    ps.setString(3, cols[2]);
                    ps.setBigDecimal(4, new java.math.BigDecimal(cols[3]));
                    ps.setDate(5, java.sql.Date.valueOf(cols[4]));
                    ps.executeUpdate();
                    processed++;
                }
            }
            System.out.println("Idempotent load processed " + processed + " rows (inserted or updated).");

            try (Statement st = conn.createStatement();
                 var rs = st.executeQuery("SELECT COUNT(*) FROM settled_trades")) {
                rs.next();
                System.out.println("Table now contains " + rs.getInt(1) + " rows total.");
            }
        }
    }
}
