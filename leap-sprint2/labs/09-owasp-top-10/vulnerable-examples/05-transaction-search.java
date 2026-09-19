// PaySprint Mobile - TransactionSearchDao.java (excerpt)

public class TransactionSearchDao {

    public List<Transaction> searchByMerchant(String merchantName) {
        String sql = "SELECT * FROM transactions WHERE merchant_name = '"
                + merchantName + "'";

        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            return mapResults(rs);
        }
    }
}
