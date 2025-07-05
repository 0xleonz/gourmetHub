<script>
  import Orders from './Orders.svelte';
  import Reservations from './Reservations.svelte';
  export let orders = [];
  export let reservations = [];
</script>

<section>
  <h2>Órdenes</h2>
  <Orders {orders} />
  <h2>Reservaciones</h2>
  <Reservations {reservations} />
</section>