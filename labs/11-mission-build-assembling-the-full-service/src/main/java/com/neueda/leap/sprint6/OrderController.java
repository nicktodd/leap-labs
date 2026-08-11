package com.neueda.leap.sprint6;

import com.neueda.leap.sprint6.domain.*;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.util.NoSuchElementException;

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
        // TODO 1: look up instrument by ticker
        InstrumentRow instrumentRow = accountMapper.findInstrument(dto.ticker());
        if (instrumentRow == null) {
            throw new NoSuchElementException("unknown ticker: " + dto.ticker());
        }

        // TODO 2: look up existing holding (may be null)
        HoldingRow holdingRow = accountMapper.findHolding(accountId, dto.ticker());
        double currentQuantity = (holdingRow != null) ? holdingRow.getQuantity() : 0.0;

        // TODO 3: compute current portfolio value (simplified)
        double currentPortfolioValue = currentQuantity * dto.price();

        // TODO 4: validate the order
        OrderRequest request = new OrderRequest(dto.quantity(), dto.price(), dto.isBuy());
        ValidationResult result = orderValidator.validate(request, currentQuantity, currentPortfolioValue, RISK_LIMIT);
        if (!result.isValid()) {
            throw new OrderRejectedException(result.getReason());
        }

        // TODO 5: apply the order and persist the updated holding
        Holding holding = new Holding(currentQuantity);
        holdingUpdater.applyOrder(holding, dto.isBuy(), dto.quantity());
        double newQuantity = holding.getQuantity();

        if (holdingRow == null) {
            accountMapper.insertHolding(accountId, instrumentRow.getInstrumentId(), newQuantity);
        } else {
            accountMapper.updateHoldingQuantity(holdingRow.getHoldingId(), newQuantity);
        }

        // TODO 6: calculate fee
        Instrument instrument = instrumentFactory.create(instrumentRow.getAssetClass().toUpperCase(), dto.ticker());
        double fee = instrument.calculateFee(request.tradeValue());

        // TODO 7: return 200 OK
        return ResponseEntity.ok(new OrderResponseDto("ACCEPTED", fee, newQuantity));
    }
}
