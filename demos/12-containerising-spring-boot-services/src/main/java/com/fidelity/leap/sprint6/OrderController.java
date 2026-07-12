package com.fidelity.leap.sprint6;

import com.fidelity.leap.sprint6.domain.*;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.util.NoSuchElementException;

// Every earlier module in this sprint meets here:
//   Module 4  - REST resource shape:      POST /accounts/{accountId}/orders
//   Module 6  - DTO + Bean Validation:     @Valid OrderRequestDto
//   Module 7  - MyBatis persistence:       AccountMapper, against the real Sprint 3 schema
//   Module 9  - JWT security:              @AuthenticationPrincipal Jwt (SecurityConfig protects this)
//   Module 10 - Centralised error handling: every failure below throws, never returns an ad-hoc body
// domain.* (OrderValidator, HoldingUpdater, InstrumentFactory, Feeable) is Sprint 5,
// Module 13, completely unchanged - see shared/mission-brief.md.
@RestController
@RequestMapping("/accounts/{accountId}/orders")
public class OrderController {

    // A real risk limit would come from the client's own record - hardcoded
    // here to keep the demo focused on assembly, not on adding yet another
    // table lookup.
    private static final double RISK_LIMIT = 2_000_000.0;

    private final AccountMapper accountMapper;
    private final OrderValidator orderValidator = new OrderValidator();
    private final HoldingUpdater holdingUpdater = new HoldingUpdater();
    private final InstrumentFactory instrumentFactory = new InstrumentFactory();

    public OrderController(AccountMapper accountMapper) {
        this.accountMapper = accountMapper;
    }

    @PostMapping
    public ResponseEntity<OrderResponseDto> submitOrder(@PathVariable int accountId,
                                                          @Valid @RequestBody OrderRequestDto dto,
                                                          @AuthenticationPrincipal Jwt jwt) {
        InstrumentRow instrument = accountMapper.findInstrument(dto.ticker());
        if (instrument == null) {
            throw new NoSuchElementException("no such instrument: " + dto.ticker());
        }

        HoldingRow existingHolding = accountMapper.findHolding(accountId, dto.ticker());
        double currentQuantity = existingHolding == null ? 0.0 : existingHolding.getQuantity();

        // Simplified for this demo: real portfolio valuation needs live
        // market prices, which this schema doesn't carry. Using the
        // incoming order's own price against the existing holding is a
        // stand-in that keeps OrderValidator's real signature and real
        // logic exercised against real data, without fabricating a price
        // feed this sprint was never going to build.
        double currentPortfolioValue = currentQuantity * dto.price();

        OrderRequest domainRequest = new OrderRequest(dto.quantity(), dto.price(), dto.isBuy());
        ValidationResult result = orderValidator.validate(
                domainRequest, currentQuantity, currentPortfolioValue, RISK_LIMIT);

        if (!result.isValid()) {
            throw new OrderRejectedException(result.getReason());
        }

        Holding holding = new Holding(currentQuantity);
        holdingUpdater.applyOrder(holding, dto.isBuy(), dto.quantity());

        if (existingHolding == null) {
            accountMapper.insertHolding(accountId, instrument.getInstrumentId(), holding.getQuantity());
        } else {
            accountMapper.updateHoldingQuantity(existingHolding.getHoldingId(), holding.getQuantity());
        }

        Instrument instrumentObj = instrumentFactory.create(
                instrument.getAssetClass().toUpperCase(), instrument.getTicker());
        double fee = instrumentObj.calculateFee(domainRequest.tradeValue());

        return ResponseEntity.ok(new OrderResponseDto("ACCEPTED", fee, holding.getQuantity()));
    }
}
