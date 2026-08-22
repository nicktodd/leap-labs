package com.neueda.leap.sprint7;

import java.io.BufferedReader;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.Statement;

// KATA: this loader works, but it is NOT safe to rerun - running it twice
// against the same CSV double-counts every confirmation. Make it idempotent.
public class ConfirmationLoader {

    static final String URL = "jdbc:postgresql://localhost:5434/sprint7";
    static final String USER = "postgres";
    static final String PASSWORD = "leappass";

    public static void main(String[] args) throws Exception {
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            try (Statement st = conn.createStatement()) {
                // TODO 1: this table has no primary key, so the database has
                // no way to detect "this confirmation was already loaded."
                // Add a PRIMARY KEY constraint on confirmation_id.
                st.execute("""
                    CREATE TABLE IF NOT EXISTS trade_confirmations (
                        confirmation_id VARCHAR(20),
                        account_id VARCHAR(20),
                        ticker VARCHAR(20),
                        side VARCHAR(10),
                        quantity NUMERIC
                    )
                    """);
            }

            // TODO 2: this is a plain INSERT - every rerun inserts the same
            // rows again. Change it to an UPSERT: INSERT ... ON CONFLICT
            // (confirmation_id) DO UPDATE SET ... so reruns converge instead
            // of duplicating. (You'll need TODO 1's primary key for this to
            // work - ON CONFLICT needs a unique constraint to target.)
            String insertSql = "INSERT INTO trade_confirmations " +
                    "(confirmation_id, account_id, ticker, side, quantity) " +
                    "VALUES (?, ?, ?, ?, ?)";

            int processed = 0;
            try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/confirmations.csv"));
                 PreparedStatement ps = conn.prepareStatement(insertSql)) {
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
