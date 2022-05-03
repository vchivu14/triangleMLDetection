<script>
  import GraphBox from "./components/GraphBox.svelte";
  import ImageBox from "./components/ImageBox.svelte";
  import { SvelteToast } from "@zerodevx/svelte-toast";
</script>

<main>
  <div class="container">
    <GraphBox />
    <hr />
    <ImageBox />
  </div>
  <SvelteToast />
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
