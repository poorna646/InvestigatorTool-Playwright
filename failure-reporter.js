import fs from 'fs';

// Playwright prints colored text. This removes the color codes
// so our JSON file contains clean, readable text.
function stripColors(text) {
  return (text || '').replace(/\u001b\[[0-9;]*m/g, '');
}

export default class FailureReporter {
  constructor() {
    this.failures = [];
  }

  // Playwright calls this after every test attempt
  onTestEnd(test, result) {
    // Ignore tests that passed
    if (result.status !== 'failed' && result.status !== 'timedOut') return;

    this.failures.push({
      testTitle: test.title,
      file: test.location.file,
      line: test.location.line,
      status: result.status,
      retryNumber: result.retry,
      durationMs: result.duration,
            errorMessage: stripColors(
        result.errors.map((e) => e.message).join('\n\n')
      ),
      stack: stripColors(
        result.errors.map((e) => e.stack).filter(Boolean).join('\n\n')
      ),
      errorLocation: result.errors.find((e) => e.location)?.location || null,
      attachments: result.attachments
        .filter((a) => a.path)
        .map((a) => ({ name: a.name, type: a.contentType, path: a.path })),
      timestamp: new Date().toISOString(),
    });
  }

  // Playwright calls this once, when all tests are finished
  onEnd() {
    fs.mkdirSync('failures', { recursive: true });
    fs.writeFileSync(
      'failures/failures.json',
      JSON.stringify(this.failures, null, 2)
    );
    console.log(`\nFailureReporter: saved ${this.failures.length} failure(s) to failures/failures.json`);
  }
}