#include "../Firmware/UdaraKitaBlynk/SensorLogic.h"
#include <cassert>
#include <cstdio>
int main(){
 SensorLogic s;
 s.startBaseline(0);for(int i=0;i<60;i++)s.sample(100+(i%2));
 assert(s.finishBaseline());assert(s.baseline==100.5f);
 s.baseline=100;
 s.update(0,true,140,1.3,1.15,10000);
 s.update(9999,true,140,1.3,1.15,10000);assert(!s.elevated);
 s.update(10000,true,140,1.3,1.15,10000);assert(s.elevated);
 s.update(20000,true,120,1.3,1.15,10000);assert(s.elevated);
 s.update(21000,true,110,1.3,1.15,10000);assert(s.elevated);
 s.update(31000,true,110,1.3,1.15,10000);assert(!s.elevated);
 // Interrupted excursion must not accumulate 10s over separate events.
 s.update(40000,true,140,1.3,1.15,10000);s.update(45000,true,120,1.3,1.15,10000);
 s.update(50000,true,140,1.3,1.15,10000);s.update(55000,true,140,1.3,1.15,10000);assert(!s.elevated);
 s.update(60000,true,140,1.3,1.15,10000);assert(s.elevated);
 s.update(60001,false,140,1.3,1.15,10000);assert(!s.elevated&&!s.pending);
 // Timer rollover still respects the hold interval.
 s.update(0xfffffff0,true,140,1.3,1.15,10000);s.update(9984,true,140,1.3,1.15,10000);assert(s.elevated);
 s.startBaseline(0);for(int i=0;i<60;i++)s.sample(i%2?200:20);assert(!s.finishBaseline());assert(s.baseline==0);
 s.startBaseline(0);for(int i=0;i<60;i++)s.sample(0);assert(!s.finishBaseline());
 s.startBaseline(0);for(int i=0;i<10;i++)s.sample(100);assert(!s.finishBaseline());
 s.startBaseline(0);for(int i=0;i<60;i++)s.sample(1023);assert(!s.finishBaseline());
 puts("PASS: baseline, unstable/invalid/short samples, hysteresis, hold time, interrupted excursion, sensor invalidation, millis rollover.");
}

