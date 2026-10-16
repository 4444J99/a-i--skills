# GCP Pricing Cheatsheet

*Prices are approximate and vary by region. Always verify at cloud.google.com/pricing.*

## Compute Engine (us-central1)

### Standard VMs (per hour)

| Type | vCPU | RAM | On-Demand | Spot |
|------|------|-----|-----------|------|
| e2-micro | 0.25 | 1GB | $0.008 | $0.002 |
| e2-small | 0.5 | 2GB | $0.017 | $0.005 |
| e2-medium | 1 | 4GB | $0.034 | $0.010 |
| e2-standard-2 | 2 | 8GB | $0.067 | $0.020 |
| e2-standard-4 | 4 | 16GB | $0.134 | $0.040 |
| e2-standard-8 | 8 | 32GB | $0.268 | $0.080 |
| n2-standard-2 | 2 | 8GB | $0.097 | $0.029 |
| n2-standard-4 | 4 | 16GB | $0.194 | $0.058 |
| n2-highmem-2 | 2 | 16GB | $0.131 | $0.039 |

### Monthly Estimates

| Type | On-Demand/mo | Spot/mo | 1yr CUD | 3yr CUD |
|------|--------------|---------|---------|---------|
| e2-medium | ~$25 | ~$7 | ~$16 | ~$11 |
| e2-standard-4 | ~$98 | ~$29 | ~$62 | ~$43 |
| n2-standard-4 | ~$142 | ~$42 | ~$89 | ~$62 |

### GPUs (per hour, in addition to VM)

| GPU | On-Demand | Spot |
|-----|-----------|------|
| NVIDIA T4 | $0.35 | $0.11 |
| NVIDIA V100 | $2.48 | $0.74 |
| NVIDIA A100 40GB | $3.67 | $1.10 |

---

## Cloud Storage (per GB/month)

| Class | Storage | Retrieval | Min Duration |
|-------|---------|-----------|--------------|
| Standard | $0.020 | Free | None |
| Nearline | $0.010 | $0.01/GB | 30 days |
| Coldline | $0.004 | $0.02/GB | 90 days |
| Archive | $0.0012 | $0.05/GB | 365 days |

**Operations:**
- Class A (write): $0.05 per 10K ops
- Class B (read): $0.004 per 10K ops

**Network egress:**
- Within same region: Free
- Between regions: $0.01-0.02/GB
- To internet: $0.12/GB (first 1TB)

---

## Cloud Run

| Resource | Price |
|----------|-------|
| vCPU-second | $0.00002400 |
| GB-second | $0.00000250 |
| Requests | $0.40 per million |

**Free tier:** 
- 2 million requests/month
- 360,000 GB-seconds
- 180,000 vCPU-seconds

**Example monthly cost:**
- 1M requests, avg 500ms, 1 vCPU, 512MB = ~$5-10

---

## Cloud Functions

| Tier | Invocations | Compute (GB-s) | Network |
|------|-------------|----------------|---------|
| Free | 2M/month | 400K GB-s | 5GB |
| Paid | $0.40/M | $0.0000025/GB-s | $0.12/GB |

---

## BigQuery

**Storage:**
- Active: $0.020/GB/month
- Long-term (>90 days): $0.010/GB/month

**Queries:**
- On-demand: $5.00/TB scanned
- Flat-rate: $2,000/month for 100 slots

**Streaming inserts:** $0.010 per 200MB

**Free tier:** 
- 10GB storage
- 1TB queries/month

---

## Cloud SQL (MySQL, us-central1)

| Instance | vCPU | RAM | $/hour | $/month |
|----------|------|-----|--------|---------|
| db-f1-micro | shared | 0.6GB | $0.0150 | ~$11 |
| db-g1-small | shared | 1.7GB | $0.0500 | ~$36 |
| db-n1-standard-1 | 1 | 3.75GB | $0.0965 | ~$70 |
| db-n1-standard-2 | 2 | 7.5GB | $0.1930 | ~$140 |

**Storage:** $0.170/GB/month (SSD)
**Backups:** $0.080/GB/month

---

## Firestore

| Operation | Price |
|-----------|-------|
| Document reads | $0.036 per 100K |
| Document writes | $0.108 per 100K |
| Document deletes | $0.012 per 100K |
| Storage | $0.108/GB/month |

**Free tier:**
- 50K reads/day
- 20K writes/day
- 1GB storage

---

## Networking

### Egress

| Destination | Price/GB |
|-------------|----------|
| Same zone | Free |
| Same region, different zone | $0.01 |
| Different region (Americas) | $0.01 |
| Different region (cross-continent) | $0.02-0.08 |
| Internet (first 1TB) | $0.12 |
| Internet (1-10TB) | $0.11 |
| Internet (10TB+) | $0.08 |

### Load Balancing

| Type | Price |
|------|-------|
| Forwarding rule | $0.025/hour (~$18/mo) |
| Data processed | $0.008-0.012/GB |

---

## Committed Use Discounts

| Term | Discount |
|------|----------|
| 1 year | 37% |
| 3 year | 55% |

Applies to: Compute Engine, Cloud SQL, GKE

---

## Quick Estimates

**Simple web app:**
- Cloud Run + Cloud SQL (small) + Storage
- ~$50-100/month

**ML training setup:**
- GPU VM (T4) + Storage
- Spot: ~$100-300/month
- On-demand: ~$400-1000/month

**Data pipeline:**
- Cloud Functions + BigQuery + Storage
- ~$20-50/month for moderate use

**Development environment:**
- e2-small spot + minimal storage
- ~$10-20/month
