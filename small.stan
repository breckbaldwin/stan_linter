data {
  int<lower = 0> N;
  vector[N] x;
  vector[N] y;
}

parameters {
  real alpha;
  real beta;
  real<lower=0> sigma;
}

model {
  alpha ~ normal(5,10);
  beta ~ normal(5, 10);
  sigma ~ normal(5, 10);
  for(i in 1:N) {
    y[i] ~ normal(alpha + beta * x[i], sigma);
  }
}
