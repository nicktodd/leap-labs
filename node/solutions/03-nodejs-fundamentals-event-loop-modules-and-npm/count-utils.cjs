function countByOutcome(attempts) {
  let successCount = 0;
  let failCount = 0;
  for (const { outcome } of attempts) {
    if (outcome === "success") {
      successCount++;
    } else {
      failCount++;
    }
  }
  return { successCount, failCount };
}

module.exports = { countByOutcome };
