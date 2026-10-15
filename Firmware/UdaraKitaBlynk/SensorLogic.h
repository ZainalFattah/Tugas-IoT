#pragma once
#include <stdint.h>
#include <math.h>

// Logika terpisah agar keputusan sensor bisa diuji tanpa perangkat.
struct SensorLogic {
  float baseline = 0;
  bool elevated = false, pending = false, collecting = false;
  uint32_t since = 0, started = 0, count = 0;
  double sum = 0, squares = 0;
  void startBaseline(uint32_t now) {
    collecting = true; started = now; count = 0; sum = squares = 0;
    baseline = 0; elevated = pending = false;
  }
  void sample(float value) {
    if (collecting) { sum += value; squares += value * value; ++count; }
  }
  bool finishBaseline() {
    collecting = false;
    if (count < 20) return false;
    double mean = sum / count;
    double variance = fmax(0.0, squares / count - mean * mean);
    if (mean < 3 || mean >= 1000 || sqrt(variance) / mean > .10) return false;
    baseline = mean; return true;
  }
  void update(uint32_t now, bool valid, float adc, float on, float off, uint32_t hold) {
    if (!valid || baseline < 3 || collecting) { pending = elevated = false; return; }
    float r = adc / baseline;
    bool candidate = elevated ? r < off : r > on;
    if (!candidate) { pending = false; return; }
    if (!pending) { pending = true; since = now; }
    if (uint32_t(now - since) >= hold) { elevated = !elevated; pending = false; }
  }
};

