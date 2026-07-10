package com.fidelity.leap.sprint6;

import java.util.List;

// XML-based configuration: no annotations here at all. The SQL lives in
// HoldingMapper.xml, matched to this interface purely by namespace (the
// fully-qualified interface name) and method name. Better for longer,
// multi-table SQL - it reads like SQL, not like a Java string.
public interface HoldingMapper {

    List<Holding> findByClientId(int clientId);
}
