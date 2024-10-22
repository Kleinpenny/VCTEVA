<template>
  <v-container>
    <v-row>
      <v-col cols="12" v-for="player in players" :key="player.id">
        <v-card
            class="mx-auto player-card"
            dark
            :style="{ background: 'linear-gradient(to right, #1a202c, #2d3748)' }"
        >
          <v-row no-gutters>
            <v-col cols="4">
              <v-img
                  :src="player.imageUrl"
                  :alt="player.name"
                  height="120"
                  cover
              ></v-img>
            </v-col>
            <v-col cols="8">
              <v-card-text>
                <v-row align="center" class="fill-height">
                  <v-col>
                    <p class="text-h5 font-weight-bold yellow--text text-uppercase">
                      {{ player.name }}
                    </p>
                    <p class="text-subtitle-1 grey--text text--lighten-1">
                      {{ player.position }}
                    </p>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-col>
          </v-row>
          <div class="player-card-footer"></div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'PlayerList',
  data() {
    return {
      players: [
        { id: 1, name: 'NARUHITEL', position: 'Striker', imageUrl: '/path/to/naruhitel.jpg' },
        { id: 2, name: 'VEXPERT', position: 'Midfielder', imageUrl: '/path/to/vexpert.jpg' },
        // Add more players here
      ],
    }
  },
}
</script>

<style scoped>
.player-card {
  transition: box-shadow 0.3s ease-in-out;
}
.player-card:hover {
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.player-card-footer {
  height: 4px;
  background: linear-gradient(to right, #f6e05e, #ed8936, #ed64a6);
}
</style>