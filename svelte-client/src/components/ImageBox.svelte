<script>
  import axios from "axios";
  let avatar, fileinput;
  import { toast } from '@zerodevx/svelte-toast'

  const onFileSelected = (e) => {
    let image = e.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onload = (e) => {
      avatar = e.target.result;
    };
  };

  $: submit = async () => {
    const imagebox = document.getElementById("imagebox");
    const form = document.getElementById("formPredict");
    const formData = new FormData(form);
    axios
      .post("http://localhost:5000/test", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        toast.push(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };
</script>

<div class="container jxgbox imagebox" id="imagebox">
  <div class="row">
    <div class="col-md-4">
      <h4>Upload Image</h4>

      {#if avatar}
        <img class="avatar" src={avatar} alt="d" />
      {:else}
        <img
          class="avatar"
          src="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png"
          alt=""
        />
      {/if}
      <div
        class="chan"
        on:click={() => {
          fileinput.click();
        }}
      />
    </div>
  </div>
  <div class="row">
    <div class="col-md-10">
      <form id="formPredict" on:submit|preventDefault={submit}>
          <div id="app">
            <input
              name="file"
              type="file"
              on:change={(e) => onFileSelected(e)}
              bind:this={fileinput}
            />
          </div>
          <br>
          <div id="app">
            <button type="submit">Submit</button>
          </div>
      </form>
    </div>
  </div>
  <div class="row" />
</div>

<style>
  .imagebox {
    width: 400px;
    height: 400px;
  }
  #app {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-flow: column;
  }
  .avatar {
    display: flex;
    height: 200px;
    width: 200px;
  }
</style>
