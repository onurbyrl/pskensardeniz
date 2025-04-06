const { createApp } = Vue

const app = createApp({
   data() {
      return {
         sepet:[],
         sepetCount:0,
         sepetTotal:0,
         seansSepet:[],
         seansSepetCount:0,
         seansSepetTotal:0,
         seansSecenek:1,
         sepetToplam:0,
         kuponDurum:"",
         kuponİndirim:0,
         ozelIndirim:0,
         ozelIndirimOran:0,
         checkoutContract:false
      }
   },
   methods:{
      sepetListe(){
         let self = this;
         axios.get("ajax.php", { params:{ action: "sepetListe" }}).then((response) => {
            self.sepet = response.data.sepet;
            self.sepetCount = response.data.sepetCount;
            self.sepetTotal = response.data.sepetTotal;
            self.ozelIndirim = response.data.ozelIndirim;
            self.ozelIndirimOran = response.data.ozelIndirimOran;

         }).catch((error) => {
            console.log(error);
         });
      },
      sepetUrunSil(indis){
         let self = this;
         axios.post("ajax.php",{action:"sepetUrunSil",indis:indis}).then((response) => {
            self.sepetListe();
            this.sepetAraToplam();
         }).catch((error) => {
            console.log(error);
         });
      },
      sepetUrunEkle(id){
         let self = this;
         axios.post("ajax.php",{action:"sepetUrunEkle",uygulama:id}).then((response) => {
            if(response.data.status == "success"){
               self.sepetListe();
               Swal.fire({
                  icon: 'success',
                  title: 'Sepete Eklendi!',
                  text: ''
               });
               this.sepetAraToplam();
            }else if(response.data.status == "already"){
               Swal.fire({
                  icon: 'warning',
                  title: 'Sepette Mevcut!',
                  text: ''
               });
               this.sepetAraToplam();
            }else{
               Swal.fire({
                  icon: 'warning',
                  title: 'Sepete Eklenmedi!',
                  text: 'Uygulama sepete eklenmedi, lütfen tekrar deneyin.'
               });
            }
         }).catch((error) => {
            console.log(error);
         });
      },

      seansSec(seans,paket){
         let self = this;
         self.seansSecenek = seans;
         $(".seansfiyat").text(paket+"₺");
      },
      
      seansSepetListe(){
         let self = this;
         axios.get("ajax.php", { params:{ action: "seansSepetListe" }}).then((response) => {
            self.seansSepet = response.data.seansSepet;
            self.seansSepetCount = response.data.seansSepetCount;
            self.seansSepetTotal = response.data.seansSepetTotal;
         }).catch((error) => {
            console.log(error);
         });
      },
      seansSepeteEkle(seansid,seanspaket){
         let self = this;
         axios.post("ajax.php",{action:"seansSepeteEkle",seansid:seansid,paket:seanspaket}).then((response) => {
            if(response.data.status == "success"){
               self.sepetListe();
               Swal.fire({
                  icon: 'success',
                  title: 'Sepete Eklendi!',
                  text: ''
               });
               this.seansSepetListe();
               this.sepetAraToplam();
            }else if(response.data.status == "already"){
               Swal.fire({
                  icon: 'warning',
                  title: 'Sepette Mevcut!',
                  text: ''
               });
               this.sepetAraToplam();
            }else{
               Swal.fire({
                  icon: 'warning',
                  title: 'Sepete Eklenmedi!',
                  text: 'Seans sepete eklenmedi, lütfen tekrar deneyin.'
               });
            }
         }).catch((error) => {
            console.log(error);
         });
      },
      seansSepetUrunSil(indis){
         let self = this;
         axios.post("ajax.php",{action:"seansSepetUrunSil",indis:indis}).then((response) => {
            self.sepetListe();
            self.seansSepetListe();
            
         }).catch((error) => {
            console.log(error);
         });
      },

      sepetAraToplam(){
         setTimeout(()  => {
            let self = this;

            if(self.seansSepetTotal <= 0 || self.seansSepetTotal == undefined){
               self.seansSepetTotal = 0;
            }

            if(self.sepetTotal <= 0 || self.sepetTotal == undefined){
               self.sepetTotal = 0;
            }


            if(self.seansSepetCount <= 0 || self.seansSepetCount == undefined){
               self.seansSepetCount = 0;
            }

            if(self.sepetCount <= 0 || self.sepetCount == undefined){
               self.sepetCount = 0;
            }



            self.sepetToplam = parseFloat(self.seansSepetTotal) + parseFloat(self.sepetTotal);
            self.sepetCount = self.seansSepetCount + self.sepetCount;

         },300);
      },
      kuponKontrol(){
         let kupon = this.$refs.kupon.value;
         axios.post("ajax.php",{action:"kuponKontrol",kupon:kupon}).then((response) => {
            if(response.data.status == "active"){
               this.sepetToplam = this.sepetToplam - response.data.kuponİndirim;
               this.kuponİndirim = response.data.kuponİndirim;
               this.kuponDurum = "active";
            }else{
               this.kuponDurum = "error";
            }
         }).catch((error) => {
            console.log(error);
         });
      },
      kuponSifirla(){
         this.sepetToplam = parseFloat(this.sepetToplam) + parseFloat(this.kuponİndirim);
         this.kuponDurum = "";
         this.kuponİndirim = 0;
         this.$refs.kupon.value = "";
         axios.post("ajax.php",{action:"kuponSıfırla"}).then((response) => {
            
         }).catch((error) => {
            console.log(error);
         });
      }

   },
   mounted(){
      this.sepetListe();
      this.seansSepetListe();
      this.sepetAraToplam();
   }

}).mount("#app");