package com.neueda.leap.mission.service;

import com.neueda.leap.mission.service.domain.*;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.util.NoSuchElementException;

// KATA: assemble everything the last five modules built into one endpoint.
// Every piece you need already exists and already works:
//   - domain.OrderValidator, domain.HoldingUpdater, domain.InstrumentFactory (from the Java week, unchanged)
//   - AccountMapper (Module 7's MyBatis, against the real Sprint 3 schema)
//   - SecurityConfig (Module 9) already protects this controller - you don't touch it
//   - GlobalExceptionHandler (Module 10) already handles everything you throw
//
// Your job is ONLY the orchestration in submitOrder below.
@RestController
@RequestMapping("/accounts/{accountId}/orders")
public class OrderController {

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
        // TODO 1: look up the instrument by dto.ticker() via accountMapper.findInstrument(...).
        //         If it's null, throw new NoSuchElementException(...) - the ticker doesn't exist.

        // TODO 2: look up the account's existing holding for this ticker via
        //         accountMapper.findHolding(accountId, dto.ticker()). It may be null (no
        //         holding yet) - treat that as a current quantity of 0.0.

        // TODO 3: compute currentPortfolioValue as currentQuantity * dto.price() (a
        //         deliberate simplification - see the demo guide for why).

        // TODO 4: build a domain.OrderRequest from the DTO, and call
        //         orderValidator.validate(request, currentQuantity, currentPortfolioValue,
        //         RISK_LIMIT). If the result isn't valid, throw
        //         new OrderRejectedException(result.getReason()).

        // TODO 5: build a domain.Holding from the current quantity, call
        //         holdingUpdater.applyOrder(holding, dto.isBuy(), dto.quantity()), then
        //         persist the new quantity - insertHolding(...) if there was no existing
        //         holding, updateHoldingQuantity(...) if there was.

        // TODO 6: use instrumentFactory.create(...) (assetClass, uppercased) to get a
        //         domain.Instrument, and call calculateFee(request.tradeValue()) for the fee.

        // TODO 7: return ResponseEntity.ok(new OrderResponseDto("ACCEPTED", fee, newQuantity)).

        throw new UnsupportedOperationException("TODO: implement submitOrder");
    }
}
