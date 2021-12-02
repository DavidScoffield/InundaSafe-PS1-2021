<template>
  <div style="height: auto; width: 70%; margin: auto">
    <h1>Zonas inundables</h1>
    <br />

    <l-map :zoom="zoom" :center="center" style="height: 500px">
      <l-tile-layer :url="url" />

      <!-- Se dibujan las zonas inundables -->
      <l-polygon
        :lat-lngs="getCoordinateList(prueba.coordenadas)"
        :color="prueba.color"
      ></l-polygon>
    </l-map>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LPolygon } from "@vue-leaflet/vue-leaflet";

export default {
  name: "FloodZones",

  components: {
    LMap,
    LTileLayer,
    LPolygon,
  },

  data() {
    return {
      zoom: 12.5,
      center: latLng(-34.9187, -57.956),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      showDescription: false,
      floodZones: [],
      currentFloodZonePage: 0,
      prueba: {
        nombre: "Berisso",
        color: "#78849D",
        coordenadas: [
          {
            lat: "-34.82720050210121",
            long: "-57.87408828735352",
          },
          {
            lat: "-34.83030279257369",
            long: "-57.87546157836914",
          },
          {
            lat: "-34.83382798079101",
            long: "-57.87683486938477",
          },
          {
            lat: "-34.83636602285396",
            long: "-57.8782081604004",
          },
          {
            lat: "-34.83735301808148",
            long: "-57.87872314453126",
          },
          {
            lat: "-34.83876299073662",
            long: "-57.879753112792976",
          },
          {
            lat: "-34.8400319454781",
            long: "-57.88061141967774",
          },
          {
            lat: "-34.841889000902036",
            long: "-57.882077896501876",
          },
          {
            lat: "-34.844144821246005",
            long: "-57.882592880632735",
          },
          {
            lat: "-34.84680163436547",
            long: "-57.88421630859376",
          },
          {
            lat: "-34.84792948494094",
            long: "-57.88438796997071",
          },
          {
            lat: "-34.84962123182082",
            long: "-57.88490295410157",
          },
          {
            lat: "-34.85145391835838",
            long: "-57.88576126098633",
          },
          {
            lat: "-34.852722677433675",
            long: "-57.88696289062501",
          },
          {
            lat: "-34.854132386793104",
            long: "-57.88816452026368",
          },
          {
            lat: "-34.85582400614023",
            long: "-57.889022827148445",
          },
          {
            lat: "-34.85737462665221",
            long: "-57.889537811279304",
          },
          {
            lat: "-34.85892521793584",
            long: "-57.89022445678712",
          },
          {
            lat: "-34.859770982680025",
            long: "-57.89056777954102",
          },
          {
            lat: "-34.861321528791464",
            long: "-57.891769409179695",
          },
          {
            lat: "-34.86273109080081",
            long: "-57.89297103881837",
          },
          {
            lat: "-34.86385872301499",
            long: "-57.89382934570313",
          },
          {
            lat: "-34.86540919206474",
            long: "-57.89434432983399",
          },
          {
            lat: "-34.86695963188314",
            long: "-57.895030975341804",
          },
          {
            lat: "-34.86794626018399",
            long: "-57.89554595947266",
          },
          {
            lat: "-34.868932876647",
            long: "-57.89640426635742",
          },
          {
            lat: "-34.86865098743696",
            long: "-57.8946876525879",
          },
          {
            lat: "-34.869073820889646",
            long: "-57.89279937744141",
          },
          {
            lat: "-34.86851004246955",
            long: "-57.89194107055665",
          },
          {
            lat: "-34.86738247403301",
            long: "-57.89056777954102",
          },
          {
            lat: "-34.866254890134904",
            long: "-57.88970947265626",
          },
          {
            lat: "-34.86456348529766",
            long: "-57.88833618164063",
          },
          {
            lat: "-34.8630130003038",
            long: "-57.88747787475587",
          },
          {
            lat: "-34.861321528791464",
            long: "-57.88627624511719",
          },
          {
            lat: "-34.859348101394986",
            long: "-57.88541793823243",
          },
          {
            lat: "-34.85892521793584",
            long: "-57.88473129272462",
          },
          {
            lat: "-34.85864329442194",
            long: "-57.88284301757813",
          },
          {
            lat: "-34.85906617933046",
            long: "-57.88061141967774",
          },
          {
            lat: "-34.86047577999055",
            long: "-57.87872314453126",
          },
          {
            lat: "-34.86288412455835",
            long: "-57.87717819213868",
          },
          {
            lat: "-34.863447941548955",
            long: "-57.87649154663087",
          },
          {
            lat: "-34.86513936932944",
            long: "-57.87408828735352",
          },
          {
            lat: "-34.86598507017437",
            long: "-57.87048339843751",
          },
          {
            lat: "-34.86725360513483",
            long: "-57.86825180053712",
          },
          {
            lat: "-34.86852212052676",
            long: "-57.86790847778321",
          },
          {
            lat: "-34.86894495464212",
            long: "-57.86739349365235",
          },
          {
            lat: "-34.870747609928245",
            long: "-57.86455012159423",
          },
          {
            lat: "-34.87102949195052",
            long: "-57.86231852369384",
          },
          {
            lat: "-34.87159325309587",
            long: "-57.859571941662594",
          },
          {
            lat: "-34.871875132218925",
            long: "-57.85545206861571",
          },
          {
            lat: "-34.87229794909151",
            long: "-57.8521905024536",
          },
          {
            lat: "-34.87257982579855",
            long: "-57.849787243176266",
          },
          {
            lat: "-34.87342545012115",
            long: "-57.846868999768056",
          },
          {
            lat: "-34.874552935688016",
            long: "-57.84618235426024",
          },
          {
            lat: "-34.87517304099755",
            long: "-57.84350937581622",
          },
          {
            lat: "-34.87545490784701",
            long: "-57.83973282552325",
          },
          {
            lat: "-34.87559584090933",
            long: "-57.83578461385333",
          },
          {
            lat: "-34.87489117318164",
            long: "-57.83389633870684",
          },
          {
            lat: "-34.87390462821523",
            long: "-57.83235138631427",
          },
          {
            lat: "-34.87164962383643",
            long: "-57.828574836021296",
          },
          {
            lat: "-34.870381156693114",
            long: "-57.827373206382624",
          },
          {
            lat: "-34.86981738723677",
            long: "-57.825828253990046",
          },
          {
            lat: "-34.869535501059026",
            long: "-57.8234249947127",
          },
          {
            lat: "-34.86925361391491",
            long: "-57.822395026450984",
          },
          {
            lat: "-34.868267001300296",
            long: "-57.82050675130451",
          },
          {
            lat: "-34.86742132392294",
            long: "-57.81964844441974",
          },
          {
            lat: "-34.86671658613143",
            long: "-57.819133460288874",
          },
          {
            lat: "-34.86301963335572",
            long: "-57.82730944105425",
          },
          {
            lat: "-34.859405229039325",
            long: "-57.83228669897654",
          },
          {
            lat: "-34.85827753576692",
            long: "-57.83400331274607",
          },
          {
            lat: "-34.856022102843",
            long: "-57.838123185792945",
          },
          {
            lat: "-34.85404854830851",
            long: "-57.84189973608592",
          },
          {
            lat: "-34.85165202558364",
            long: "-57.84704957739451",
          },
          {
            lat: "-34.85038324999858",
            long: "-57.84876619116404",
          },
          {
            lat: "-34.84587188947378",
            long: "-57.85494600073435",
          },
          {
            lat: "-34.84460302476501",
            long: "-57.8576925827656",
          },
          {
            lat: "-34.84291117472225",
            long: "-57.859924180666",
          },
          {
            lat: "-34.83980935931925",
            long: "-57.86438737646677",
          },
          {
            lat: "-34.83825840778491",
            long: "-57.866618974367164",
          },
          {
            lat: "-34.83572042406191",
            long: "-57.868850572267554",
          },
          {
            lat: "-34.832618337701206",
            long: "-57.871768815675765",
          },
          {
            lat: "-34.831067250692115",
            long: "-57.87194047705272",
          },
          {
            lat: "-34.82909309769527",
            long: "-57.87331376806834",
          },
        ],
        id: 6,
      },
    };
  },

  methods: {
    innerClick() {
      // oculta o muestra la descripción del recorrido de evacuación

      this.showDescription = !this.showDescription;
    },

    fetchFloodZonesPage(page = 1) {
      // consulta a la api de puntos de encuentro para obtener la página solicitada
      fetch(`${process.env.VUE_APP_BASE_URL}/zonas-inundables?pagina=${page}`)
        .then((response) => {
          return response.json();
        })
        .then((json) => {
          this.floodZones = json.zonas;
        })
        .catch((e) => {
          console.log(e);
        });
    },

    // fetchEvacuationRoutePage(page = 1) {
    //   // consulta a la api de recorridos de evacuación para obtener la página solicitada

    //   fetch(
    //     `https://admin-grupo24.proyecto2021.linti.unlp.edu.ar/api/recorridos-evacuacion?pagina=${page}`
    //   )
    //     .then((response) => {
    //       return response.json();
    //     })
    //     .then((json) => {
    //       this.evacuationRoutes = json.recorridos;
    //     })
    //     .catch((e) => {
    //       console.log(e);
    //     });
    // },

    getCoordinateList(coordinates) {
      // retorna un listado con las coordenadas [lat, long] de la zona inundable

      // return coordinates.map((coor) => [coor.lat, coor.long]);
      var coordinateList = [];
      for (let latLong of coordinates) {
        coordinateList.push([latLong.lat, latLong.long]);
      }
      return coordinateList;
    },
  },

  created() {
    // hook created donde se cargan los puntos de encuentro y recorridos de evacuación
    // con la información de la primer página de los listados

    this.fetchFloodZonePage(1);
    // this.fetchEvacuationRoutePage(1);
  },
};
</script>