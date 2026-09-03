/* ===========================================================================
   PronoStat — Store de datos compartido entre módulos
   El dataset vive en el navegador (sessionStorage). Arquitectura stateless:
   cada módulo lee el dataset y envía las columnas relevantes a su solve_api.
   =========================================================================== */
(function (global) {
  const KEY = 'pronostat_dataset';

  const Store = {
    /* dataset = { source, sheet, columns:[{name,type}], rows:[{col:val,...}], meta } */
    save(dataset) {
      dataset.savedAt = new Date().toISOString();
      sessionStorage.setItem(KEY, JSON.stringify(dataset));
      this.refreshBadge();
    },
    get() {
      const raw = sessionStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : null;
    },
    has() { return !!sessionStorage.getItem(KEY); },
    clear() { sessionStorage.removeItem(KEY); this.refreshBadge(); },

    columns() { const d = this.get(); return d ? d.columns : []; },
    columnNames() { return this.columns().map(c => c.name); },
    numericColumns() { return this.columns().filter(c => c.type === 'numérico').map(c => c.name); },

    /* Devuelve un array con los valores de una columna (respeta el orden de filas). */
    values(name) {
      const d = this.get(); if (!d) return [];
      return d.rows.map(r => r[name]);
    },
    /* Valores numéricos válidos (descarta null/NaN). */
    numericValues(name) {
      return this.values(name).map(Number).filter(v => !Number.isNaN(v) && v !== null);
    },

    refreshBadge() {
      const el = document.getElementById('ds-status');
      if (!el) return;
      const d = this.get();
      if (d) {
        el.className = 'ds-status ds-loaded';
        el.textContent = `✔ ${d.rows.length} filas · ${d.columns.length} campos`;
        el.title = `${d.source || 'dataset'}${d.sheet ? ' · ' + d.sheet : ''}`;
      } else {
        el.className = 'ds-status ds-empty';
        el.textContent = 'Sin datos cargados';
      }
    }
  };

  /* --------- Utilidades compartidas --------- */
  const Util = {
    fmt(x, dec = 4) {
      if (x === null || x === undefined || (typeof x === 'number' && Number.isNaN(x))) return '—';
      if (typeof x !== 'number') return x;
      if (!isFinite(x)) return x > 0 ? '∞' : '-∞';
      if (Math.abs(x) !== 0 && (Math.abs(x) < 1e-4 || Math.abs(x) >= 1e7))
        return x.toExponential(3);
      return x.toLocaleString('es-CL', { maximumFractionDigits: dec });
    },
    async postJSON(url, payload) {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || ('HTTP ' + res.status));
      return data;
    },
    /* Descarga un archivo devuelto por un endpoint POST (blob). */
    async downloadPost(url, payload, filename) {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        let msg = 'HTTP ' + res.status;
        try { const j = await res.json(); msg = j.error || msg; } catch (e) {}
        throw new Error(msg);
      }
      const blob = await res.blob();
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(a.href);
    },
    /* Llena un <select> con nombres de columnas. */
    fillColumnSelect(sel, names, { onlyNumeric = false, selectedIndex = 0 } = {}) {
      if (!sel) return;
      sel.innerHTML = '';
      if (!names.length) {
        sel.innerHTML = '<option value="">(sin columnas)</option>';
        return;
      }
      names.forEach((n, i) => {
        const o = document.createElement('option');
        o.value = n; o.textContent = n;
        sel.appendChild(o);
      });
      sel.selectedIndex = Math.min(selectedIndex, names.length - 1);
    },
    /* Muestra un aviso "carga datos primero" si no hay dataset. */
    requireDataset(containerId) {
      if (Store.has()) return true;
      const c = document.getElementById(containerId);
      if (c) c.innerHTML =
        '<div class="alert alert-warn">Aún no has cargado datos. ' +
        'Ve al módulo <a href="/datos/"><b>1 · Datos</b></a> para importar tu Excel o CSV. ' +
        'También puedes usar el ejemplo incluido en cada módulo.</div>';
      return false;
    }
  };

  global.PronoStat = Store;
  global.PSU = Util;
  document.addEventListener('DOMContentLoaded', () => Store.refreshBadge());
})(window);
