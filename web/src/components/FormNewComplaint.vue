<template>
    <div class="container">
        <Title>Realizar una denuncia</Title>
        <form
            @submit="save"
            method="post"
        >
            <p class="d-flex" style="color:red" v-show="name_error">{{ name_error }}</p>
            <p class="d-flex" style="color:green" v-show="is_correct">{{ is_correct }}</p>
            <div class="form-group">
                <label class="d-flex" for="titulo">Título (*) </label>
                <input id="titulo" ref="title_error" class="form-control" placeholder="Ingrese un título" v-model="titulo">
                <p class="d-flex" style="color:red" v-if="title_error">El título solo puede estar compuesto de letras</p>
                <br>
            </div>
            <div class="form-group">
                <label class="d-flex" for="categoria">Categoría (*) </label>
                <select id="categoria" ref="category_error" class="form-control" v-model="categoria_id">
                    <option disabled value="">Seleccione una categoría</option>
                    <option v-for="(category, index) in categories" :value="category.id" :key="index">{{category.nombre}}</option>                   
                </select>
                <p class="d-flex" style="color:red" v-if="category_error">La categoría es incorrecta</p>
                <br>
            </div>
            <div class="form-group">
                <label class="d-flex" for="descripcion">Descripción (*) </label>
                <textarea id="descripcion" ref="description_error" style="resize: none" rows="3" class="form-control" maxlength= 400 v-model="descripcion" placeholder="Ingrese una descripción"></textarea>
                <p class="d-flex" style="color:red" v-show="description_error">{{ description_error }}</p>
            </div>
            <div class="form-group">
                <label class="d-flex" for="apellido">Apellido (*) </label>
                <input id="apellido" ref="last_name_error" class="form-control" placeholder="Ingrese un apellido" v-model="apellido_denunciante">
                <p class="d-flex" style="color:red" v-if="last_name_error">El apellido solo puede estar compuesto de letras</p>
                <br>
            </div>
            <div class="form-group">
                <label class="d-flex" for="nombre">Nombre (*) </label>
                <input id="nombre" ref="first_name_error" class="form-control" placeholder="Ingrese un nombre" v-model="nombre_denunciante">
                <p class="d-flex" style="color:red" v-if="first_name_error">El nombre solo puede estar compuesto de letras</p>
                <br>
            </div>
            <div class="form-group">
                <label class="d-flex" for="telefono">Teléfono (*) </label>
                <input id="telefono" ref="phone_error" class="form-control" placeholder="Ingrese un télefono" v-model="telcel_denunciante">
                <p class="d-flex" style="color:red" v-if="phone_error">El teléfono solo puede estar compuesto de números</p>
                <br>
            </div>
            <div class="form-group">
                <label class="d-flex" for="email">Email (*) </label>
                <input id="email" ref="email_error" class="form-control" placeholder="Ingrese un email" v-model="email_denunciante">
                <p class="d-flex" style="color:red" v-if="email_error">El email debe ser válido</p>
                <br>   
            </div>     
            <i class="d-flex">Campos obligatorios (*)</i>

            <l-map style="height: 350px" :zoom="zoom" :center="center" @click="onClickMap">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker v-if="coordenadas" :lat-lng="coordenadas" ></l-marker>
            </l-map>
            <br>
            <button style="float:right" class="button-gradient btn-lg" type="submit">Aceptar</button>
        </form>
    </div>
</template>

<script>
import { latLng } from "leaflet";
import {LMap, LTileLayer, LMarker} from '@vue-leaflet/vue-leaflet';
import Title from "./Title.vue"

export default {
    name: 'FormNewComplaint',
    components: {
        LMap,
        LTileLayer,
        LMarker, 
        Title
    },
    data () {
        return {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        zoom: 13,
        center: [-34.9187, -57.956],
        coordenadas: latLng(),
        categories: [],
        titulo: "",
        categoria_id: "",
        descripcion: "",
        apellido_denunciante: "",
        nombre_denunciante: "",
        telcel_denunciante: "",
        email_denunciante: "",
        name_error: "",
        is_correct: "",
        title_error: false,
        category_error: false,
        description_error: "",
        last_name_error: false,
        first_name_error: false,
        phone_error: false,
        email_error: false,
        };
    },
    created(){
        fetch(`${process.env.VUE_APP_BASE_URL}/categories`)
        .then((res) => {
            return res.json()
        })
        .then((resJson) =>{
            this.categories = resJson
        })
        .catch(() =>{
            console.log("catch")
        })
    },
    methods: {
        onClickMap(e){
            if(e.latlng){
                this.coordenadas = e.latlng
            }
        },
        save(e) {
            e.preventDefault()
            this.name_error = ""
            this.is_correct = ""
            this.title_error = false
            this.category_error = false
            this.description_error = ""
            this.last_name_error = false
            this.first_name_error = false
            this.phone_error = false
            this.email_error = false
            if(!this.validate()){
                return false
            }
            let coordenadas = String(this.coordenadas.lat) + ", " + String(this.coordenadas.lng)
            let telefono = String(this.telcel_denunciante)
            const requestComplaint = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ categoria_id: this.categoria_id, coordenadas: coordenadas, apellido_denunciante: this.apellido_denunciante, nombre_denunciante: this.nombre_denunciante, telcel_denunciante: telefono, email_denunciante: this.email_denunciante, titulo: this.titulo, descripcion: this.descripcion })
            };
            fetch(`${process.env.VUE_APP_BASE_URL}/denuncias/`, requestComplaint)
            .then(() => {
                this.$refs.title_error.focus()
                this.is_correct = "La denuncia se creó correctamente"
                this.cleanUp()
            })
            .catch(() => {
                this.name_error = "Por favor corrija los errores"
            })
        },
        validate(){
            if (!this.coordenadas || !this.titulo || !this.categoria_id || !this.descripcion || !this.apellido_denunciante || !this.nombre_denunciante || !this.telcel_denunciante || !this.email_denunciante){
                this.$refs.title_error.focus()
                this.name_error = "Por favor complete todos los campos"
                return false
            }
            if(!(/^[a-zA-Z ]+$/.test(this.titulo))){
                this.$refs.title_error.focus()
                this.title_error = true
                return false
            }
            if(!(/^[a-zA-Z0-9 ]+$/.test(this.descripcion))){
                this.$refs.description_error.focus()
                this.description_error = "La descripción no puede contener caracteres especiales, solo letras y/o números"
                return false
            }
            if(!(/^[a-zA-Z ]+$/.test(this.apellido_denunciante))){
                this.$refs.last_name_error.focus()
                this.last_name_error = true
                return false
            }
            if(!(/^[a-zA-Z ]+$/.test(this.nombre_denunciante))){
                this.$refs.first_name_error.focus()
                this.first_name_error = true
                return false
            }
            
            if(!(/^[\d]+$/.test(this.telcel_denunciante))){
                this.$refs.phone_error.focus()
                this.phone_error = true
                return false
            }
            if(!(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.email_denunciante))){
                this.$refs.email_error.focus()
                this.email_error = true
                return false
            }
            if(this.descripcion.length > 400){
                this.$refs.description_error.focus()
                this.description_error = "La descripción no puede ser tan larga"
                return false
            }
            return true
        },
        cleanUp(){
            this.titulo = ""
            this.categoria_id = ""
            this.descripcion = ""
            this.apellido_denunciante = ""
            this.nombre_denunciante = ""
            this.telcel_denunciante = ""
            this.email_denunciante = ""
            this.coordenadas = latLng()
            setTimeout(() => this.is_correct = "", 7000)
        }
    },
    watch: {
        titulo: function(){
            if (!this.titulo){
                this.title_error = false
            }
            else if(!(/^[a-zA-Z ]+$/.test(this.titulo))){
                this.title_error = true
            }
            else{
                this.title_error = false
            }
        },
        descripcion: function(){
            if (!this.descripcion){
                this.description_error = ""
            }
            else if(!(/^[a-zA-Z0-9 ]+$/.test(this.descripcion))){
                this.description_error = "La descripción no puede contener caracteres especiales, solo letras y/o números"
            }
            else{
                this.description_error = ""
            }
        },
        apellido_denunciante: function(){
            if (!this.apellido_denunciante){
                this.last_name_error = false
            }
            else if(!(/^[a-zA-Z ]+$/.test(this.apellido_denunciante))){
                this.last_name_error = true
            }
            else{
                this.last_name_error = false
            }
        },
        nombre_denunciante: function(){
            if (!this.nombre_denunciante){
                this.first_name_error = false
            }
            else if(!(/^[a-zA-Z ]+$/.test(this.nombre_denunciante))){
                this.first_name_error = true
            }
            else{
                this.first_name_error = false
            }
        },
        telcel_denunciante: function(){
            if (!this.telcel_denunciante){
                this.phone_error = false
            }
            else if(!(/^[\d]+$/.test(this.telcel_denunciante))){
                this.phone_error = true
            }
            else{
                this.phone_error = false
            }
        },
        email_denunciante: function(){
            if (!this.email_denunciante){
                this.email_error = false
            }
            else if(!(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.email_denunciante))){
                this.email_error = true
            }
            else{
                this.email_error = false
            }
        }
    }
  }

</script>