package com.neueda.leap.paysprint;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class TransactionSearchDao {

    private Connection connection;

    public TransactionSearchDao(Connection connection) {
        this.connection = connection;
    }

    // VULNERABILITY (A05): the original version built SQL by string
    // concatenation with user input, a classic SQL injection.
    //
    // FIX (A05): a parameterised query with a bind parameter, not string
    // concatenation or escaping. Note: a Copilot suggestion that merely
    // escapes quotes in merchantName should be rejected, escaping is fragile;
    // parameter binding removes the entire class of problem.
    public List<Transaction> searchByMerchant(String merchantName) throws SQLException {
        String sql = "SELECT id, merchant_name, amount FROM transactions WHERE merchant_name = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, merchantName);
            try (ResultSet rs = stmt.executeQuery()) {
                return mapResults(rs);
            }
        }
    }

    private List<Transaction> mapResults(ResultSet rs) throws SQLException {
        List<Transaction> results = new ArrayList<>();
        while (rs.next()) {
            results.add(new Transaction(
                    rs.getLong("id"),
                    rs.getString("merchant_name"),
                    rs.getDouble("amount")));
        }
        return results;
    }
}
