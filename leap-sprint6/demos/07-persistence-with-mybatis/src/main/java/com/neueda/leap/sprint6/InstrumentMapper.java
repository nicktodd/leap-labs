package com.neueda.leap.sprint6;

import org.apache.ibatis.annotations.Select;

// Annotation-based configuration: the SQL lives right next to the method it
// belongs to, in the Java file. Good for short, simple queries - there's
// nowhere else to look.
public interface InstrumentMapper {

    // #{ticker} is a PARAMETERISED placeholder, not string concatenation -
    // MyBatis turns this into a JDBC PreparedStatement with a bound
    // parameter, the same protection against SQL injection Sprint 3 covered
    // for raw JDBC/SQL.
    @Select("SELECT ticker, name, asset_class, currency FROM instruments WHERE ticker = #{ticker}")
    Instrument findByTicker(String ticker);
}
