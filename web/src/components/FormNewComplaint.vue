<template>
    <div>
        <form
            @submit="save"
            method="post"
        >
            <p style="color:red" v-show="name_error">{{ name_error }}</p>
            <label for="">Título (*) </label>
            <input required pattern = "^[a-zA-Z ]+$" placeholder="Ingrese un título" v-model="titulo">
            <br>
            <label for="">Categoría (*) </label>
            <select required v-model="categoria_id">
                <option disabled value="">Seleccione una categoría</option>
                <option value="2">Basural</option>
                <option value="1">Alcantarilla tapada</option>
            </select>
            <br>
            <label for="">Descripción (*) </label>
            <textarea required pattern= "^[a-zA-Z0-9 ]+$" maxlength= 400 v-model="descripcion" placeholder="Ingrese una descripción"></textarea>
            <br>
            <label for="">Apellido (*) </label>
            <input required pattern = "^[a-zA-Z ]+$" placeholder="Ingrese un apellido" v-model="apellido_denunciante">
            <br>
            <label for="">Nombre (*) </label>
            <input required pattern = "^[a-zA-Z ]+$" placeholder="Ingrese un nombre" v-model="nombre_denunciante">
            <br>
            <label for="">Télefono (*) </label>
            <input required type="number" pattern = "^[\d]+$" placeholder="Ingrese un télefono" v-model="telcel_denunciante">
            <br>
            <label for="">Email (*) </label>
            <input required type="email" placeholder="Ingrese un email" v-model="email_denunciante">
            <br>        
            <i>Campos obligatorios (*)</i>

            <l-map style="height: 350px" :zoom="zoom" :center="center" @click="onClickMap">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker :lat-lng="coordenadas" ></l-marker>
            </l-map>
            <br>
            <button type="submit">Aceptar</button>
        </form>
    </div>
</template>
<style>
    /* Chrome, Safari, Edge, Opera */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
    }

    /* Firefox */
    input[type=number] {
    -moz-appearance: textfield;
    }
</style>

<script>
import { latLng } from "leaflet";
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
        coordenadas: latLng(),
        titulo: "",
        categoria_id: "",
        descripcion: "",
        apellido_denunciante: "",
        nombre_denunciante: "",
        telcel_denunciante: "",
        email_denunciante: "",
        name_error:"",
        };
    },
    methods: {
        onClickMap(e){
            if(e.latlng){
                this.coordenadas = e.latlng
            }
        },
        save(e) {
            e.preventDefault()
            if(!this.validate()){
                return false
            }
            console.log(this.coordenadas)
            let categoria = Number(this.categoria_id)
            let coordenadas = String(this.coordenadas.lat) + ", " + String(this.coordenadas.lng)
            let telefono = String(this.telcel_denunciante)
            console.log(coordenadas)
            //console.log(JSON.stringify({categoria_id: this.categoria_id, coordenadas: this.coordenadas, apellido_denunciante: this.apellido_denunciante, nombre_denunciante: this.nombre_denunciante, telcel_denunciante: this.telcel_denunciante, email_denunciante: this.email_denunciante, titulo: this.titulo, descripcion: this.descripcion}))
            const requestComplaint = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ categoria_id: categoria, coordenadas: coordenadas, apellido_denunciante: this.apellido_denunciante, nombre_denunciante: this.nombre_denunciante, telcel_denunciante: telefono, email_denunciante: this.email_denunciante, titulo: this.titulo, descripcion: this.descripcion })
            };
            console.log(JSON.stringify({categoria_id: this.categoria_id, coordenadas: coordenadas, apellido_denunciante: this.apellido_denunciante, nombre_denunciante: this.nombre_denunciante, telcel_denunciante: this.telcel_denunciante, email_denunciante: this.email_denunciante, titulo: this.titulo, descripcion: this.descripcion}))
            fetch("http://localhost:5000/api/denuncias/", requestComplaint)
            .catch(() => {
                console.log("errrorrrrrrrrrrrrrr")
                this.name_error = "Por favor corrija los errores"
            })
        },
        validate(){
            if (!this.coordenadas || !this.titulo || !this.categoria_id || !this.descripcion || !this.apellido_denunciante || !this.nombre_denunciante || !this.telcel_denunciante || !this.email_denunciante){
                this.name_error = "Por favor complete todos los campos"
                return false
            }
            if(!(/^[a-zA-Z ]+$/.test(this.titulo))){
                this.name_error = "El título solo puede estar compuesto de letras"
                return false
            }
            if(this.categoria_id != "1" && this.categoria_id != "2"){
                this.name_error = "La categoría es incorrecta"
                return false
            }
            if(!(/^[a-zA-Z0-9 ]+$/.test(this.descripcion))){
                this.name_error = "La descripción no puede contener caracteres especiales, solo letras y/o números"
                return false
            }
            if(!(/^[a-zA-Z ]+$/.test(this.apellido_denunciante))){
                this.name_error = "El apellido solo puede estar compuesto de letras"
                return false
            }
            if(!(/^[a-zA-Z ]+$/.test(this.nombre_denunciante))){
                this.name_error = "El nombre solo puede estar compuesto de letras"
                return false
            }
            
            if(!(/^[\d]+$/.test(this.telcel_denunciante))){
                this.name_error = "El teléfono solo puede estar compuesto de números"
                return false
            }
            if(!(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.email_denunciante))){
                this.name_error = "El email debe ser válido"
                return false
            }
            if(this.descripcion.length > 400){
                this.name_error = "La descripción no puede ser tan larga"
                return false
            }
            return true
        }
    }
  }

</script>