// KATA TODO 1: export a function countByOutcome(attempts) that returns
// { successCount, failCount } - counting attempts where outcome ===
// "success" vs anything else. Use module.exports, CommonJS style (no
// export keyword).

function countByOutcome(attempts) {
  let successCount = 0;
  let failCount = 0;
  for (const attempt of attempts) {
    if (attempt.outcome === "success") {
      successCount++;
    } else {
      failCount++;
    }
  }
  return { successCount, failCount };
}

module.exports = { countByOutcome };
