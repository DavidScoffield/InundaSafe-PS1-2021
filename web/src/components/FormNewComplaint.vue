<template>
    <div>
        
            <label for="">Título (*) </label>
            <input pattern = "^[a-zA-Z ]+$" placeholder="Ingrese un título" v-model="titulo">
            <br>
            <label for="">Categoría (*) </label>
            <select v-model="categoria_id">
                <option disabled value="">Seleccione una categoría</option>
                <option value="2">Basural</option>
                <option value="1">Alcantarilla tapada</option>
            </select>
            <br>
            <label for="">Descripción (*) </label>
            <textarea pattern= "^[a-zA-Z0-9 ]+$" maxlength= 400 v-model="descripcion" placeholder="Ingrese una descripción"></textarea>
            <br>
            <label for="">Apellido (*) </label>
            <input pattern = "^[a-zA-Z ]+$" placeholder="Ingrese un apellido" v-model="apellido_denunciante">
            <br>
            <label for="">Nombre (*) </label>
            <input pattern = "^[a-zA-Z ]+$" placeholder="Ingrese un nombre" v-model="nombre_denunciante">
            <br>
            <label for="">Télefono (*) </label>
            <input pattern = "^[\d]+$" placeholder="Ingrese un télefono" v-model="telcel_denunciante">
            <br>
            <label for="">Email (*) </label>
            <input type="email" placeholder="Ingrese un email" v-model="email_denunciante">
            <br>        

            <l-map style="height: 350px" :zoom="zoom" :center="center" @click="onClickMap">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker :lat-lng="coordenadas" ></l-marker>
            </l-map>
            <br>
            <button @click="save">Aceptar</button>
        
    </div>
</template>

<script>
import {LMap, LTileLayer, LMarker} from '@vue-leaflet/vue-leaflet';

export default {
    name: 'FormNewComplaint',
    components: {
        LMap,
        LTileLayer,
        LMarker
    },
    data () {
        return {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        zoom: 13,
        center: [-34.9187, -57.956],
        coordenadas: [],
        titulo: "",
        categoria_id: "",
        descripcion: "",
        apellido_denunciante: "",
        nombre_denunciante: "",
        telcel_denunciante: "",
        email_denunciante: "",
        };
    },
    methods: {
        onClickMap(e){
            if(e.latlng){
                this.coordenadas = e.latlng
            }
        },
        save() {
            console.log("ENTRE")
            this.categoria_id = Number(this.categoria_id)
            let coordenadas = String(this.coordenadas.lat) + ", " + String(this.coordenadas.lng)
            //console.log(JSON.stringify({categoria_id: this.categoria_id, coordenadas: this.coordenadas, apellido_denunciante: this.apellido_denunciante, nombre_denunciante: this.nombre_denunciante, telcel_denunciante: this.telcel_denunciante, email_denunciante: this.email_denunciante, titulo: this.titulo, descripcion: this.descripcion}))
            const requestComplaint = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ categoria_id: this.categoria_id, coordenadas: coordenadas, apellido_denunciante: this.apellido_denunciante, nombre_denunciante: this.nombre_denunciante, telcel_denunciante: this.telcel_denunciante, email_denunciante: this.email_denunciante, titulo: this.titulo, descripcion: this.descripcion })
            };
            fetch("http://localhost:5000/api/denuncias/", requestComplaint)
            .catch((e) => {
                console.log(e)
            })
        }
    }
}
</script>