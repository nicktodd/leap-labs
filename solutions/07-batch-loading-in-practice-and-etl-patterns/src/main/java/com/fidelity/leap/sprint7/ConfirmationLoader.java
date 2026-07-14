package com.fidelity.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.Statement;

// Idempotent: confirmation_id is a PRIMARY KEY, and the load is an UPSERT.
// Running this any number of times against the same CSV converges on the
// same 5 rows - it never duplicates.
public class ConfirmationLoader {

    static final String URL = "jdbc:postgresql://localhost:5434/sprint7";
    static final String USER = "postgres";
    static final String PASSWORD = "leappass";

    public static void main(String[] args) throws Exception {
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            try (Statement st = conn.createStatement()) {
                st.execute("""
                    CREATE TABLE IF NOT EXISTS trade_confirmations (
                        confirmation_id VARCHAR(20) PRIMARY KEY,
                        account_id VARCHAR(20),
                        ticker VARCHAR(20),
                        side VARCHAR(10),
                        quantity NUMERIC
                    )
                    """);
            }

            String upsertSql = """
                INSERT INTO trade_confirmations
                    (confirmation_id, account_id, ticker, side, quantity)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (confirmation_id) DO UPDATE SET
                    account_id = EXCLUDED.account_id,
                    ticker = EXCLUDED.ticker,
                    side = EXCLUDED.side,
                    quantity = EXCLUDED.quantity
                """;

            int processed = 0;
            try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/confirmations.csv"));
                 PreparedStatement ps = conn.prepareStatement(upsertSql)) {
                br.readLine(); // header
                String line;
                while ((line = br.readLine()) != null) {
                    String[] cols = line.split(",");
                    ps.setString(1, cols[0]);
                    ps.setString(2, cols[1]);
                    ps.setString(3, cols[2]);
                    ps.setString(4, cols[3]);
                    ps.setBigDecimal(5, new java.math.BigDecimal(cols[4]));
                    ps.executeUpdate();
                    processed++;
                }
            }
            System.out.println("Processed " + processed + " confirmations.");

            try (Statement st = conn.createStatement();
                 var rs = st.executeQuery("SELECT COUNT(*) FROM trade_confirmations")) {
                rs.next();
                System.out.println("Table now contains " + rs.getInt(1) + " rows total.");
            }
        }
    }
}
