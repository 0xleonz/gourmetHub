<script>
  export let orders = [];
</script>
{#if orders.length > 0}
  <ul>
    {#each orders as o}
      <li>
        <strong>#{o.id}</strong> – {o.status}
        {#if o.eta}
          (ETA: {o.eta}s)
        {/if}
      </li>
    {/each}
  </ul>
{:else}
  <p>No hay órdenes en cola.</p>
{/if}