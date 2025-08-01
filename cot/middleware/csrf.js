const crypto = require('crypto');
const SECRET = process.env.APP_SECRET;

// Generate a CSRF token based on current timestamp + app secret
function generateCsrf() {
  const ts = Math.floor(Date.now() / 1000);
  // HMAC-SHA256(timestamp, SECRET)
  const hmac = crypto.createHmac('sha256', SECRET)
                     .update(ts.toString())
                     .digest('hex');
  return `${ts}:${hmac}`;
}

// Validate incoming CSRF token: check HMAC and freshness (±5 minutes)
function validateCsrf(token) {
  if (!token) return false;
  const [tsStr, sig] = token.split(':');
  const ts = parseInt(tsStr, 10);
  // Recompute
  const expected = crypto.createHmac('sha256', SECRET)
                         .update(tsStr)
                         .digest('hex');
  const now = Math.floor(Date.now() / 1000);
  // Within ±300 seconds
  if (sig !== expected) return false;
  if (Math.abs(now - ts) > 300) return false;
  return true;
}

// Middleware to inject token into every rendered view
function injectCsrf(req, res, next) {
  res.locals.csrfToken = generateCsrf();
  next();
}

module.exports = { injectCsrf, validateCsrf };

