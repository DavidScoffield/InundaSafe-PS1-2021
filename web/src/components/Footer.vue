<template>
  <footer class="footer">
    <div class="footer-container">
      <svg
        width="100%"
        height="90"
        viewBox="0 0 1440 111"
        preserveAspectRatio="none"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M0 33.9399C0 30.8687 2.31913 28.2933 5.37352 27.9727L80 20.1378C160 12.1205 320 -4.29575 480 1.04909C640 6.39393 800 33.8817 960 39.6083C1120 44.9531 1280 28.5368 1360 20.1378L1433.4 12.7818C1436.93 12.4278 1440 15.2016 1440 18.7519V105C1440 108.314 1437.31 111 1434 111H1360C1280 111 1120 111 960 111C800 111 640 111 480 111C320 111 160 111 80 111H6C2.68629 111 0 108.314 0 105V33.9399Z"
          fill="url(#paint0_linear_6:213)"
        />
        <defs>
          <linearGradient
            id="paint0_linear_6:213"
            x1="-626.493"
            y1="212.288"
            x2="-424.008"
            y2="-485.445"
            gradientUnits="userSpaceOnUse"
          >
            <stop stop-color="var(--color-2)" offset="0" />
            <stop offset="1" stop-color="var(--color-1)" />
          </linearGradient>
        </defs>
      </svg>
      <p class="footer-content">
        Aplicacion Pública - <strong>InundaSafe</strong> - Proyecto de Software
      </p>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped>
.footer {
  height: 90px;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-self: flex-end;
}

.footer-container {
  position: relative;
  width: 100%;
}

.footer-content {
  padding-bottom: 0;
  margin-left: 20px;
  position: absolute;
  top: 50%;
}
</style>