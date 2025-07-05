<script>
  import { onDestroy, onMount } from 'svelte';
  import Orders from '../components/Orders.svelte';
  import Reservations from '../components/Reservations.svelte';

  let orders = [];
  let reservations = [];
  let interval;
  const API_BASE = 'http://localhost:8000'; // URL de tu backend

  async function fetchDashboard() {
    try {
      const res = await fetch(`${API_BASE}/dashboard`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const { orders: o, reservations: r } = await res.json();
      orders = o;
      reservations = r;
    } catch (err) {
      console.error('Error fetching dashboard:', err);
    }
  }

  onMount(() => {
    // Solo en cliente
    fetchDashboard();
    interval = setInterval(fetchDashboard, 3000);
  });

  onDestroy(() => {
    clearInterval(interval);
  });
</script>

<main>
  <h1>GourmetHub Dashboard</h1>
  <section>
    <h2>Órdenes</h2>
    <Orders {orders} />
  </section>
  <section>
    <h2>Reservaciones</h2>
    <Reservations {reservations} />
  </section>
</main>