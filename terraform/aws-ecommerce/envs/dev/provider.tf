terraform {
  required_version = ">= 1.6.0"         

  required_providers {
    aws = {
      source  = "hashicorp/aws"        
      version = "~> 5.0"              
    }
  }
}

# ── 2. PROVIDER BLOCK ───────────────────────────────────────────
provider "aws" {
  region = var.aws_region             

  # ── 3. DEFAULT TAGS ─────────────────────────────────────────
  default_tags {
    tags = {
      Project     = "ecommerce-platform"
      Environment = var.environment     
      ManagedBy   = "terraform"
      Owner       = "anjali"
      Repository  = "platform-engineering-blueprint"
    }
  }
}
  