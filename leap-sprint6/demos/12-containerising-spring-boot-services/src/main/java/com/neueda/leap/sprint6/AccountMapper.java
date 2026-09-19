package com.neueda.leap.sprint6;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Update;

// Module 7's two mapper styles, both in play: the joins below live in
// AccountMapper.xml (findInstrument, findHolding); the simple single-table
// writes are annotation-based, right here.
public interface AccountMapper {

    InstrumentRow findInstrument(@Param("ticker") String ticker);

    HoldingRow findHolding(@Param("accountId") int accountId, @Param("ticker") String ticker);

    @Update("UPDATE holdings SET quantity = #{quantity}, as_of_date = CURRENT_DATE " +
            "WHERE holding_id = #{holdingId}")
    void updateHoldingQuantity(@Param("holdingId") int holdingId, @Param("quantity") double quantity);

    @Insert("INSERT INTO holdings (account_id, instrument_id, quantity, as_of_date) " +
            "VALUES (#{accountId}, #{instrumentId}, #{quantity}, CURRENT_DATE)")
    void insertHolding(@Param("accountId") int accountId, @Param("instrumentId") int instrumentId,
                        @Param("quantity") double quantity);
}
