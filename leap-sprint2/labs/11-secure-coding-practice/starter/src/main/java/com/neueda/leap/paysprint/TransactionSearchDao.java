package com.neueda.leap.paysprint;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class TransactionSearchDao {

    private Connection connection;

    public TransactionSearchDao(Connection connection) {
        this.connection = connection;
    }

    public List<Transaction> searchByMerchant(String merchantName) throws SQLException {
        String sql = "SELECT id, merchant_name, amount FROM transactions "
                + "WHERE merchant_name = '" + merchantName + "'";

        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            return mapResults(rs);
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
