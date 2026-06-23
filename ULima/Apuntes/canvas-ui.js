var CanvasUI = (function () {
  'use strict';

  var COLORS = {
    bg: '#1e293b',
    surface: '#334155',
    line: '#3b82f6',
    accent: '#10b981',
    warn: '#f59e0b',
    danger: '#ef4444',
    text: '#e2e8f0',
    textMuted: '#94a3b8',
    highlight: '#f472b6',
    grid: '#1e293b'
  };

  function getContext(id) {
    var c = document.getElementById(id);
    if (!c) return null;
    var ctx = c.getContext('2d');
    var rect = c.parentElement.getBoundingClientRect();
    c.width = Math.min(rect.width - 4, 800);
    c.height = Math.min(c.width * 0.5, 360);
    ctx.clearRect(0, 0, c.width, c.height);
    return { ctx: ctx, canvas: c, W: c.width, H: c.height };
  }

  function clear(id) {
    var c = document.getElementById(id);
    if (!c) return;
    var ctx = c.getContext('2d');
    ctx.clearRect(0, 0, c.width, c.height);
  }

  function fillBg(ctx, W, H) {
    ctx.fillStyle = COLORS.bg;
    ctx.fillRect(0, 0, W, H);
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  function drawNode(ctx, x, y, w, h, label, color, sublabel) {
    roundRect(ctx, x, y, w, h, 8);
    ctx.fillStyle = color || COLORS.surface;
    ctx.fill();
    ctx.strokeStyle = COLORS.line;
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.fillStyle = COLORS.text;
    ctx.font = 'bold 13px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(label, x + w / 2, y + h / 2 - (sublabel ? 6 : 0));
    if (sublabel) {
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = '10px Inter, sans-serif';
      ctx.fillText(sublabel, x + w / 2, y + h / 2 + 14);
    }
  }

  function drawArrow(ctx, x1, y1, x2, y2, color) {
    var dx = x2 - x1, dy = y2 - y1;
    var len = Math.sqrt(dx * dx + dy * dy);
    var nx = dx / len, ny = dy / len;
    ctx.strokeStyle = color || COLORS.line;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2 - nx * 12, y2 - ny * 12);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - nx * 12 - ny * 6, y2 - ny * 12 + nx * 6);
    ctx.lineTo(x2 - nx * 12 + ny * 6, y2 - ny * 12 - nx * 6);
    ctx.closePath();
    ctx.fillStyle = color || COLORS.line;
    ctx.fill();
  }

  function drawTable(ctx, x, y, cols, rows, highlightIdx, animOffset) {
    var colW = 90, rowH = 28, headerH = 32;
    var pad = 4;
    var fullW = cols.length * colW + pad * 2;
    var fullH = (rows.length + 1) * rowH + headerH + pad * 2;
    roundRect(ctx, x, y, fullW, fullH, 6);
    ctx.fillStyle = '#0f172a';
    ctx.fill();
    ctx.strokeStyle = COLORS.surface;
    ctx.lineWidth = 1;
    ctx.stroke();
    for (var c = 0; c < cols.length; c++) {
      var cx = x + pad + c * colW;
      ctx.strokeStyle = COLORS.surface;
      ctx.strokeRect(cx, y + pad, colW, headerH);
      ctx.fillStyle = COLORS.accent;
      ctx.font = 'bold 11px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(cols[c], cx + colW / 2, y + pad + headerH / 2);
    }
    for (var r = 0; r < rows.length; r++) {
      var ry = y + pad + headerH + r * rowH;
      var isHighlight = highlightIdx !== undefined && r === highlightIdx;
      if (isHighlight) {
        ctx.fillStyle = 'rgba(59, 130, 246, 0.15)';
        ctx.fillRect(x + pad, ry, fullW - pad * 2, rowH);
      }
      for (var c2 = 0; c2 < cols.length; c2++) {
        var cx2 = x + pad + c2 * colW;
        ctx.strokeStyle = COLORS.surface;
        ctx.strokeRect(cx2, ry, colW, rowH);
        var val = rows[r][c2] !== undefined ? rows[r][c2] : '';
        ctx.fillStyle = isHighlight ? COLORS.highlight : COLORS.text;
        ctx.font = '11px JetBrains Mono, monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(String(val), cx2 + colW / 2, ry + rowH / 2);
      }
    }
  }

  function drawVenn(ctx, W, H, type) {
    var cx = W / 2, cy = H / 2 + 10;
    var r = 72;
    var offset = type === 'inner' ? 0 : 30;
    var showB = type !== 'inner';

    function drawCircle(x, y, label, color) {
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fillStyle = color || 'rgba(59, 130, 246, 0.2)';
      ctx.fill();
      ctx.strokeStyle = COLORS.line;
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.fillStyle = COLORS.text;
      ctx.font = 'bold 16px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(label, x, y);
    }

    if (type === 'inner') {
      drawCircle(cx, cy, 'A ⋂ B', 'rgba(59, 130, 246, 0.35)');
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = '12px Inter, sans-serif';
      ctx.fillText('INNER JOIN: Solo registros que coinciden en ambas tablas', cx, H - 30);
    } else if (type === 'left') {
      drawCircle(cx - offset, cy, 'A', 'rgba(59, 130, 246, 0.3)');
      drawCircle(cx + offset, cy, 'B', 'rgba(16, 185, 129, 0.15)');
      ctx.fillStyle = 'rgba(59, 130, 246, 0.25)';
      ctx.beginPath();
      ctx.arc(cx - offset, cy, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = '12px Inter, sans-serif';
      ctx.fillText('LEFT JOIN: Todos de A + coincidencias de B', cx, H - 30);
    } else if (type === 'right') {
      drawCircle(cx - offset, cy, 'A', 'rgba(59, 130, 246, 0.15)');
      drawCircle(cx + offset, cy, 'B', 'rgba(16, 185, 129, 0.3)');
      ctx.fillStyle = 'rgba(16, 185, 129, 0.25)';
      ctx.beginPath();
      ctx.arc(cx + offset, cy, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = '12px Inter, sans-serif';
      ctx.fillText('RIGHT JOIN: Todos de B + coincidencias de A', cx, H - 30);
    } else if (type === 'full') {
      drawCircle(cx - offset, cy, 'A', 'rgba(59, 130, 246, 0.25)');
      drawCircle(cx + offset, cy, 'B', 'rgba(16, 185, 129, 0.25)');
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = '12px Inter, sans-serif';
      ctx.fillText('FULL OUTER JOIN: Todos los registros de ambas tablas', cx, H - 30);
    }
  }

  function drawPipeline(ctx, W, H, stages, current, labels) {
    var n = stages.length;
    var boxW = Math.min(140, (W - 60) / n);
    var boxH = 50;
    var gap = (W - n * boxW) / (n + 1);
    var y = H / 2 - boxH / 2;
    for (var i = 0; i < n; i++) {
      var x = gap + i * (boxW + gap);
      var active = i <= current;
      drawNode(ctx, x, y, boxW, boxH, stages[i], active ? COLORS.accent : COLORS.surface, labels ? labels[i] : null);
      if (i < n - 1) {
        drawArrow(ctx, x + boxW, y + boxH / 2, x + boxW + gap, y + boxH / 2, active ? COLORS.line : COLORS.surface);
      }
    }
  }

  function drawTabAnimation(ctx, W, H, tables, currentStep) {
    fillBg(ctx, W, H);
    ctx.fillStyle = COLORS.textMuted;
    ctx.font = '12px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Paso ' + (currentStep + 1) + ' de ' + tables.length + ' — ' + tables[currentStep].title, W / 2, 24);
    var t = tables[currentStep];
    drawTable(ctx, 20, 40, t.cols, t.rows, t.highlight);
    if (t.extra) {
      ctx.fillStyle = COLORS.warn;
      ctx.font = '11px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(t.extra, 20, 40 + (t.rows.length + 1) * 28 + 50);
    }
  }

  function drawCube(ctx, W, H, labels, highlightDim) {
    var cx = W / 2 - 20, cy = H / 2 - 10;
    var size = 80;
    var depth = 40;

    function face(x, y, w, h, label, isHighlight) {
      roundRect(ctx, x, y, w, h, 4);
      ctx.fillStyle = isHighlight ? 'rgba(59, 130, 246, 0.35)' : 'rgba(51, 65, 85, 0.7)';
      ctx.fill();
      ctx.strokeStyle = isHighlight ? COLORS.highlight : COLORS.line;
      ctx.lineWidth = isHighlight ? 2 : 1;
      ctx.stroke();
      if (label) {
        ctx.fillStyle = COLORS.text;
        ctx.font = '11px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, x + w / 2, y + h / 2);
      }
    }

    face(cx - depth, cy - depth * 0.5, size, size, labels[2], highlightDim === 2);
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx - depth, cy - depth * 0.5);
    ctx.lineTo(cx - depth, cy + size - depth * 0.5);
    ctx.lineTo(cx, cy + size);
    ctx.closePath();
    ctx.fillStyle = 'rgba(30, 41, 59, 0.5)';
    ctx.fill();
    ctx.strokeStyle = COLORS.surface;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(cx + size, cy);
    ctx.lineTo(cx + size - depth, cy - depth * 0.5);
    ctx.lineTo(cx - depth, cy - depth * 0.5);
    ctx.lineTo(cx, cy);
    ctx.closePath();
    ctx.fillStyle = 'rgba(30, 41, 59, 0.5)';
    ctx.fill();
    ctx.strokeStyle = COLORS.surface;
    ctx.stroke();

    face(cx, cy, size, size, labels[0], highlightDim === 0);
  }

  function drawCluster(ctx, W, H, state) {
    fillBg(ctx, W, H);
    var nodes = [
      { x: 80, y: H / 2 - 30, label: 'Primary', status: state.primary },
      { x: W - 180, y: H / 2 - 30, label: 'Standby', status: state.standby }
    ];
    var clientY = 40;
    ctx.fillStyle = COLORS.text;
    ctx.font = '12px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Clientes', W / 2, clientY + 5);
    drawNode(ctx, W / 2 - 40, clientY - 10, 80, 30, 'App', COLORS.surface);
    drawArrow(ctx, W / 2, clientY + 25, nodes[0].x + 60, nodes[0].y + 20, state.primary === 'up' ? COLORS.accent : COLORS.danger);

    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      var color = n.status === 'up' ? COLORS.accent : COLORS.danger;
      var label = n.label + (n.status === 'up' ? ' (UP)' : ' (DOWN)');
      drawNode(ctx, n.x, n.y, 120, 45, label, color);
    }
    drawArrow(ctx, nodes[0].x + 120, nodes[0].y + 15, nodes[1].x, nodes[1].y + 15, COLORS.line);
    ctx.fillStyle = COLORS.textMuted;
    ctx.font = '11px Inter, sans-serif';
    ctx.textAlign = 'center';
    var syncLabel = state.primary === 'up' && state.standby === 'up' ? 'Sincronizando datos...' : (state.primary === 'down' ? 'FAILOVER: Standby asume el control' : 'Esperando conexion...');
    ctx.fillText(syncLabel, W / 2, nodes[0].y + 80);
  }

  function startAnimation(id, drawFn, fps) {
    var running = true;
    var frame = 0;
    function loop() {
      if (!running) return;
      var ctx = getContext(id);
      if (ctx) {
        fillBg(ctx.ctx, ctx.W, ctx.H);
        drawFn(ctx.ctx, ctx.W, ctx.H, frame);
      }
      frame++;
      setTimeout(loop, 1000 / (fps || 30));
    }
    loop();
    return { stop: function () { running = false; } };
  }

  function addControls(containerId, callbacks) {
    var container = document.getElementById(containerId);
    if (!container) return;
    var div = document.createElement('div');
    div.className = 'canvas-controls';
    if (callbacks.play) {
      var btnPlay = document.createElement('button');
      btnPlay.className = 'btn-canvas';
      btnPlay.textContent = 'Play';
      btnPlay.onclick = callbacks.play;
      div.appendChild(btnPlay);
    }
    if (callbacks.pause) {
      var btnPause = document.createElement('button');
      btnPause.className = 'btn-canvas';
      btnPause.textContent = 'Pausa';
      btnPause.onclick = callbacks.pause;
      div.appendChild(btnPause);
    }
    if (callbacks.reset) {
      var btnReset = document.createElement('button');
      btnReset.className = 'btn-canvas';
      btnReset.textContent = 'Reset';
      btnReset.onclick = callbacks.reset;
      div.appendChild(btnReset);
    }
    if (callbacks.step) {
      var btnStep = document.createElement('button');
      btnStep.className = 'btn-canvas';
      btnStep.textContent = 'Paso ' + (callbacks.stepLabel || '');
      btnStep.onclick = callbacks.step;
      div.appendChild(btnStep);
    }
    container.appendChild(div);
  }

  function observeAndRun(canvasId, runFn) {
    var el = document.getElementById(canvasId);
    if (!el) return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          runFn();
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.3 });
    observer.observe(el);
  }

  return {
    COLORS: COLORS,
    getContext: getContext,
    clear: clear,
    fillBg: fillBg,
    drawNode: drawNode,
    drawArrow: drawArrow,
    drawTable: drawTable,
    drawVenn: drawVenn,
    drawPipeline: drawPipeline,
    drawTabAnimation: drawTabAnimation,
    drawCube: drawCube,
    drawCluster: drawCluster,
    startAnimation: startAnimation,
    addControls: addControls,
    observeAndRun: observeAndRun
  };
})();
