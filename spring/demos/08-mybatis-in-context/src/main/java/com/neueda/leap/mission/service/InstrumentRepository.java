package com.neueda.leap.mission.service;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

// Compare this to Module 7's InstrumentMapper. No SQL anywhere - not
// even a method body. Spring Data JPA generates the query from the
// method name at startup ("query derivation"), and JpaRepository
// already provides findById, save, delete, findAll, etc. for free.
public interface InstrumentRepository extends JpaRepository<Instrument, Integer> {

    Optional<Instrument> findByTicker(String ticker);
}
