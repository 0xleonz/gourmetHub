<script>
  export let reservations = [];
</script>
{#if reservations.length > 0}
  <ul>
    {#each reservations as r}
      <li>
        <strong>#{r.id}</strong> – {r.name} ({r.party_size}) – {r.status}
        {#if r.eta}
          (ETA: {r.eta}s)
        {/if}
      </li>
    {/each}
  </ul>
{:else}
  <p>No hay reservaciones en cola.</p>
{/if}
