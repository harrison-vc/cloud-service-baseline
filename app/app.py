import os
import time
import logging
from fastapi import FastAPI, HTTPException, Response

# Structured Logging Setup
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
)
logger = logging.getLogger("service-baseline")

app = FastAPI(title="Cloud Service Baseline")

# Simulation variables
START_TIME = time.time()
HEALTHY = True

@app.get("/health")
async def health_check():
    """Endpoint for Load Balancer and K8s probes."""
    if not HEALTHY:
        logger.error("Health check failed - marked unhealthy")
        raise HTTPException(status_code=503, detail="Service Unavailable")
    
    uptime = time.time() - START_TIME
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "version": "1.0.0"
    }

@app.get("/api/v1/data")
async def get_data(request_id: str = "unknown"):
    """Example data endpoint with structured log tracing."""
    extra = {"request_id": request_id}
    logger.info("Processing data request", extra=extra)
    
    # Simulate work
    time.sleep(0.05)
    
    return {"data": "Cloud Service Baseline Result", "request_id": request_id}

@app.post("/admin/toggle-health")
async def toggle_health(healthy: bool):
    """Admin endpoint to simulate failure for testing."""
    global HEALTHY
    HEALTHY = healthy
    return {"status": f"Healthy set to {healthy}"}

@app.get("/api/v1/simulate-timeout")
async def simulate_timeout(delay: int = 40):
    """Endpoint to simulate slow responses for timeout testing."""
    logger.warning(f"Simulating timeout with {delay}s delay")
    time.sleep(delay)
    return {"status": "delayed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)