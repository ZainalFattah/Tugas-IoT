(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const REAL_FACTOR = 10; // 1 detik di browser = 10 detik pada urutan firmware.
  const WARMUP_SECONDS = 600;
  const BASELINE_SECONDS = 60;
  const HOLD_SECONDS = 10;
  const ON_RATIO = 1.30;
  const OFF_RATIO = 1.15;
  const parts = {
    nodemcu: ['NodeMCU V3 ESP8266', 'Pusat kendali. Firmware asli membaca DHT11 di D2, MQ-135 di A0, lalu menggerakkan LED hijau D5 dan merah D6.', []],
    mq: ['MQ-135', 'Modul asli memakai 5 V. Keluaran AO harus melalui pembagi 47 kΩ/10 kΩ sebelum A0. Nilai ADC adalah respons relatif, bukan ppm.', ['5v','gnd','adc']],
    dht: ['DHT11', 'Modul 3 pin diberi 3,3 V; DATA menuju D2/GPIO4. Letakkan jauh dari panas sensor MQ-135.', ['3v3','gnd','dht']],
    divider: ['Pembagi tegangan ADC', 'AO → 47 kΩ → titik A0; titik A0 → 10 kΩ → GND. Jika AO maksimum 5 V, tegangan titik A0 sekitar 0,88 V.', ['adc','gnd']],
    c1: ['C1 · 100 nF', 'Dari titik ADC/A0 ke GND. Kapasitor ini membantu meredam gangguan pembacaan analog.', ['adc','gnd']],
    c2: ['C2 · elko 100 µF', 'Kaki positif ke rel 5 V dan kaki negatif ke GND dekat MQ-135. Perhatikan polaritas elko.', ['5v','gnd']],
    c3: ['C3 · 100 nF', 'Dipakai di antara 3V3 dan GND untuk meredam gangguan suplai DHT11.', ['3v3','gnd']],
    pullup: ['R3 · 10 kΩ opsional', 'Resistor dari DATA DHT11 ke 3V3 hanya diperlukan bila modul belum memiliki pull-up bawaan.', ['dht','3v3']],
    leds: ['Dua LED, dua kaki masing-masing', 'D5/D6 → resistor 1 kΩ → anoda (+) LED. Katoda (−) kedua LED menuju GND bersama.', ['green','red','gnd']]
  };
  const state = {};
  function reset() {
    Object.assign(state, {seconds:0, conditioned:false, gas:310, temperature:27, humidity:62,
      baseline:null, collecting:false, baselineStarted:0, samples:[], sampleAt:0,
      elevated:false, pendingSince:null, message:'Konfirmasi masa conditioning sensor untuk mulai.'});
    $('gasSlider').value = state.gas; $('tempSlider').value = state.temperature; $('humiditySlider').value = state.humidity;
    render();
  }
  const valid = () => state.gas >= 3 && state.gas < 1000 && state.temperature >= 0 && state.temperature <= 50 && state.humidity >= 0 && state.humidity <= 100;
  const warmed = () => state.seconds >= WARMUP_SECONDS;
  function status() {
    if (!state.conditioned) return 'conditioning';
    if (!warmed()) return 'warming';
    if (!valid()) return 'sensor_error';
    if (state.collecting) return 'calibrating';
    if (state.baseline === null) return 'baseline_required';
    return state.elevated ? 'elevated' : 'normal';
  }
  const labels = {conditioning:'Conditioning',warming:'Pemanasan',sensor_error:'Sensor bermasalah',calibrating:'Mengambil baseline',baseline_required:'Baseline diperlukan',elevated:'Respons meningkat',normal:'Normal'};
  function tick(simSeconds) {
    state.seconds += simSeconds;
    if (state.collecting) {
      while (state.sampleAt + 1 <= state.seconds) { state.sampleAt += 1; state.samples.push(state.gas); }
      if (state.seconds - state.baselineStarted >= BASELINE_SECONDS) finishBaseline();
    }
    if (state.conditioned && warmed() && valid() && state.baseline !== null && !state.collecting) {
      const ratio = state.gas / state.baseline;
      const candidate = state.elevated ? ratio < OFF_RATIO : ratio > ON_RATIO;
      if (!candidate) state.pendingSince = null;
      else if (state.pendingSince === null) state.pendingSince = state.seconds;
      else if (state.seconds - state.pendingSince >= HOLD_SECONDS) {
        state.elevated = !state.elevated; state.pendingSince = null;
        state.message = state.elevated ? 'Respons MQ-135 melebihi 1,30× baseline selama 10 detik simulasi.' : 'Respons turun di bawah 1,15× baseline selama 10 detik simulasi.';
      }
    } else {state.pendingSince=null; state.elevated=false;}
    render();
  }
  function finishBaseline() {
    state.collecting = false;
    const n=state.samples.length, mean=state.samples.reduce((a,b)=>a+b,0)/Math.max(1,n);
    const variance=state.samples.reduce((a,b)=>a+(b-mean)**2,0)/Math.max(1,n);
    if (n<20 || mean<3 || mean>=1000 || Math.sqrt(variance)/mean>.10) {
      state.baseline=null; state.message='Baseline gagal: bacaan MQ-135 berubah terlalu besar. Stabilkan slider lalu ulangi.';
    } else {state.baseline=mean; state.message=`Baseline ${Math.round(mean)} ADC tersimpan untuk sesi simulasi ini.`;}
    state.samples=[];
  }
  function render() {
    const s=status(), ratio=state.baseline===null?null:state.gas/state.baseline;
    $('statusLabel').textContent=labels[s];
    $('statusDetail').textContent=s==='warming'?`Sisa ${Math.ceil((WARMUP_SECONDS-state.seconds)/10)} detik demo.`:s==='calibrating'?`Sisa ${Math.ceil((BASELINE_SECONDS-(state.seconds-state.baselineStarted))/10)} detik demo.`:state.message;
    $('adcValue').textContent=state.gas; $('gasReadout').textContent=state.gas;
    $('tempValue').textContent=state.temperature; $('tempReadout').textContent=state.temperature;
    $('humidityValue').textContent=state.humidity; $('humidityReadout').textContent=state.humidity;
    $('ratioSummary').textContent=ratio===null?'Rasio belum tersedia':`${ratio.toFixed(2)}× dari baseline ${Math.round(state.baseline)} ADC`;
    const green=s==='normal', red=s==='elevated';
    $('greenBulb').setAttribute('fill',green?'#29e683':'#8cc8aa');
    $('redBulb').setAttribute('fill',red?'#ff555c':'#e4a7a0');
    $('greenBulb').style.filter=green?'drop-shadow(0 0 12px #16c96b)':'';
    $('redBulb').style.filter=red?'drop-shadow(0 0 12px #ef4a51)':'';
    $('indicatorLabel').textContent=green?'Hijau menyala':red?'Merah menyala':'Keduanya mati';
    $('indicatorDetail').textContent=green?'Rasio di bawah ambang bahaya':red?'Respons sensor meningkat':'Menunggu kondisi siap';
    $('conditionButton').disabled=state.conditioned;
    $('conditionButton').textContent=state.conditioned?'Terkonfirmasi ✓':'Konfirmasi demo';
    $('warmupButton').disabled=!state.conditioned||warmed();
    $('warmupButton').textContent=warmed()?'Selesai ✓':'Percepat demo';
    $('baselineButton').disabled=!state.conditioned||!warmed()||state.collecting||!valid();
    $('baselineButton').textContent=state.collecting?'Mengambil…':'Mulai kalibrasi';
    $('warmupHint').textContent=warmed()?'Pemanasan selesai · model demo':'10 menit alat asli · 60 detik demo';
    $('baselineHint').textContent=state.collecting?`${Math.max(0,Math.ceil((BASELINE_SECONDS-(state.seconds-state.baselineStarted))/10))} detik demo tersisa`:'60 detik alat asli · 6 detik demo';
    const data=[['V0','Suhu',`${state.temperature} °C`],['V1','Kelembapan',`${state.humidity} %`],['V2','MQ ADC',`${state.gas}`],['V3','Rasio',ratio===null?'—':`${ratio.toFixed(2)}×`],['V4','Status',labels[s]],['V5','Conditioning',state.conditioned?'Sudah':'Belum'],['V6','Perintah baseline',state.collecting?'Aktif':'Siap'],['V7','Baseline',state.baseline===null?'—':`${Math.round(state.baseline)} ADC`],['V8','Waktu aktif',`${Math.floor(state.seconds)} s`]];
    $('streams').replaceChildren(...data.map(([pin,name,value])=>{const el=document.createElement('div');el.className='stream';const title=document.createElement('span');title.textContent=name;const val=document.createElement('strong');val.textContent=value;const foot=document.createElement('small');foot.textContent=pin;el.append(title,val,foot);return el;}));
  }
  [['gasSlider','gas'],['tempSlider','temperature'],['humiditySlider','humidity']].forEach(([id,key])=>$(id).addEventListener('input',e=>{state[key]=Number(e.target.value);render();}));
  $('conditionButton').addEventListener('click',()=>{state.conditioned=true;state.message='Conditioning dikonfirmasi untuk simulasi. Di alat asli, MQ-135 baru perlu lebih dari 48 jam.';render();});
  $('warmupButton').addEventListener('click',()=>{state.seconds=Math.max(state.seconds,WARMUP_SECONDS);state.message='Pemanasan dipercepat hanya untuk demonstrasi.';render();});
  $('baselineButton').addEventListener('click',()=>{state.collecting=true;state.baseline=null;state.elevated=false;state.baselineStarted=state.seconds;state.sampleAt=state.seconds;state.samples=[];state.message='Jaga nilai MQ-135 stabil selama pengambilan baseline.';render();});
  $('resetButton').addEventListener('click',reset);
  function selectPart(key){const item=parts[key],info=$('componentInfo');document.querySelectorAll('.component').forEach(el=>el.classList.toggle('active',el.dataset.part===key));document.querySelectorAll('.wire').forEach(el=>el.classList.toggle('selected',item[2].includes(el.dataset.net)));$('circuit').classList.toggle('circuit-focus',item[2].length>0);info.querySelector('p').replaceChildren();const strong=document.createElement('strong');strong.textContent=item[0]+'. ';info.querySelector('p').append(strong,document.createTextNode(item[1]));}
  document.querySelectorAll('.component').forEach(el=>{el.addEventListener('click',()=>selectPart(el.dataset.part));el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectPart(el.dataset.part);}});});
  reset();
  let previous=performance.now();setInterval(()=>{const now=performance.now();const delta=Math.min((now-previous)/1000,1);previous=now;tick(delta*REAL_FACTOR);},100);
})();
