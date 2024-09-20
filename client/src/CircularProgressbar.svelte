<script>
  export let value = 0;
  export let maxValue = 100;
  export let text = '';
  export let strokeWidth = 8;
  export let styles = {};

  $: percentage = (value / maxValue) * 100;
  $: strokeDasharray = `${percentage} ${100 - percentage}`;

  const radius = 75.5 - strokeWidth / 2;
  const circumference = radius * 2 * Math.PI;
</script>

<svg class="circular-progressbar" viewBox="0 0 151 151" width="151" height="151">
  <circle
    class="circular-progressbar__background"
    cx="75.5"
    cy="75.5"
    r={radius}
    fill="#D9D9D9"
    stroke="#4b5563"
    stroke-width={strokeWidth}
  />
  <circle
    class="circular-progressbar__progress"
    cx="75.5"
    cy="75.5"
    r={radius}
    fill="none"
    stroke={styles.path?.stroke || '#584294'}
    stroke-width={strokeWidth}
    stroke-dasharray={strokeDasharray}
    stroke-dashoffset={circumference * ((100 - percentage) / 100)}
    transform="rotate(-90 75.5 75.5)"
  />
  {#if text}
    <text
      x="75.5"
      y="75.5"
      text-anchor="middle"
      dominant-baseline="central"
      fill={styles.text?.fill || '#584294'}
      font-size={styles.text?.fontSize || '36px'}
      font-weight="normal"
      font-family="Inter"
    >
      {text}
    </text>
  {/if}
</svg>

<style>
  .circular-progressbar {
    width: 151px;
    height: 151px;
  }

  .circular-progressbar__progress {
    transition: stroke-dashoffset 0.3s ease;
  }
</style>