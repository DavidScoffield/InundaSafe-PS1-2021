<template>
    <div>
        <label for="">Título: </label>
        <input placeholder="Ingrese un título" v-model="titulo">
        <br>
        <label for="">Categoría: </label>
        <select v-model="categoria_id">
            <option disabled value="">Seleccione una categoría</option>
            <option value="2">Basural</option>
            <option value="1">Alcantarilla tapada</option>
        </select>
        <br>
        <label for="">Descripción: </label>
        <input placeholder="Ingrese una descripción" v-model="descripcion">
        <br>
        <label for="">Apellido: </label>
        <input placeholder="Ingrese un apellido" v-model="apellido_denunciante">
        <br>
        <label for="">Nombre: </label>
        <input placeholder="Ingrese un nombre" v-model="nombre_denunciante">
        <br>
        <label for="">Télefono: </label>
        <input placeholder="Ingrese un télefono" v-model="telcel_denunciante">
        <br>
        <label for="">email_denunciante: </label>
        <input placeholder="Ingrese un email" v-model="email_denunciante">
        <br>        
    </div>
    <div>
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
            console.log(e)
        },
        save(){
            alert(`coordenadas: ${this.coordenadas}, titulo: ${this.titulo}, categoria: ${this.categoria_id}, descripcion: ${this.descripcion}, apellido_denunciante: ${this.apellido_denunciante}, nombre_Denunciante: ${this.nombre_denunciante}, telcel_denunciante: ${this.telcel_denunciante}, email_denunciante: ${this.email_denunciante}`)
        }
    }
}
</script>