package com.neueda.leap.sprint6;

import org.apache.ibatis.annotations.Select;

public interface AdvisorMapper {

    @Select("SELECT advisor_id, name, region FROM advisors WHERE advisor_id = #{advisorId}")
    Advisor findById(int advisorId);
}
