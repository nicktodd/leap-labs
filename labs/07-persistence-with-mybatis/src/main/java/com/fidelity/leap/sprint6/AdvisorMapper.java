package com.fidelity.leap.sprint6;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface AdvisorMapper {

    @Select("SELECT advisor_id AS advisorId, name, region FROM advisors WHERE advisor_id = #{advisorId}")
    Advisor findById(int advisorId);
}
