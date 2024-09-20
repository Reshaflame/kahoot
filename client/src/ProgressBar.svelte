<script>
    export let current = 0;
    export let total = 5;

    $: progress = (current / total) * 100;
</script>

<div class="progress-container">
    <div class="progress-bar" style="width: {progress}%"></div>
</div>

<style>
    .progress-container {
        width: 100%;
        height: 10px;
        background-color: #e0e0e0;
        border-radius: 5px;
        margin-bottom: 20px;
    }

    .progress-bar {
        height: 100%;
        background-color: #fdd1d9;
        border-radius: 5px;
        transition: width 0.3s ease;
    }
</style>