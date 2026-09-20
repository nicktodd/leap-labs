package com.neueda.leap.mission.stream;

import java.io.BufferedReader;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.Statement;

// A naive batch load: plain INSERT, no regard for whether this row was
// already loaded by a previous run. Run this class TWICE against the same
// CSV to see the consequence.
public class NaiveLoader {

    static final String URL = "jdbc:postgresql://localhost:5434/missionstream";
    static final String USER = "postgres";
    static final String PASSWORD = "leappass";

    public static void main(String[] args) throws Exception {
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            try (Statement st = conn.createStatement()) {
                st.execute("""
                    CREATE TABLE IF NOT EXISTS settled_trades_naive (
                        settlement_id VARCHAR(20),
                        account_id VARCHAR(20),
                        ticker VARCHAR(20),
                        quantity NUMERIC,
                        settled_date DATE
                    )
                    """);
            }

            String insertSql = "INSERT INTO settled_trades_naive " +
                    "(settlement_id, account_id, ticker, quantity, settled_date) " +
                    "VALUES (?, ?, ?, ?, ?)";

            int loaded = 0;
            try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/settlements.csv"));
                 PreparedStatement ps = conn.prepareStatement(insertSql)) {
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
                    loaded++;
                }
            }
            System.out.println("Naive load inserted " + loaded + " rows.");

            try (Statement st = conn.createStatement();
                 var rs = st.executeQuery("SELECT COUNT(*) FROM settled_trades_naive")) {
                rs.next();
                System.out.println("Table now contains " + rs.getInt(1) + " rows total.");
            }
        }
    }
}
