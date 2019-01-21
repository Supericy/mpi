<html>
<head>
    <title>MPI Auction</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/vuetify/dist/vuetify.min.css" rel="stylesheet">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">

    <style>
        [v-cloak] { display: none; }
    </style>
</head>
<body>
<div v-cloak id="app">
    <v-app id="inspire">
        <v-content>
            <v-container fluid>
                <v-layout align-center justify-center>
                    <v-flex xs12>
                        <v-card class="ma-0 pa-0">
                            <v-toolbar dark color="success" style="text-align: center">
                                <v-toolbar-title>New Subscription</v-toolbar-title>
                                <v-spacer></v-spacer>
                            </v-toolbar>
                            <v-card-text>
                                <v-form ref="form" v-model="valid"
      lazy-validation>
                                    <v-text-field
                                            class="ma-0 pa-0"
                                            prepend-icon="person"
                                            v-model="email"
                                            label="Email"
                                            type="text"
                                            :rules="[v => !!v || 'Item is required']"
                                            required
                                    ></v-text-field>
                                    <v-text-field
                                            class="ma-0 pa-0"
                                            prepend-icon="person"
                                            v-model="searchMinimumYear"
                                            label="Minimum Year"
                                            type="text"
                                    ></v-text-field>
                                    <v-text-field
                                            class="ma-0 pa-0"
                                            prepend-icon="person"
                                            v-model="searchModel"
                                            label="Model"
                                            type="text"
                                    ></v-text-field>
                                </v-form>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="primary" @click="subscribe">Subscribe</v-btn>
                            </v-card-actions>
                        </v-card>

                        <v-card style="margin-top: 16px">
                            <v-toolbar dark color="info">
                                <v-toolbar-title>Subscriptions</v-toolbar-title>
                                <v-spacer></v-spacer>
                            </v-toolbar>
                            <v-card-text>
                                <table style="width: 100%">
                                    <tr v-for="subscription in subscriptions.subscriptions">
                                        <td>{{subscription.email}}</td>
                                        <td>{{subscription.search}}</td>
                                        <td style="text-align: right">
                                            <v-btn color="error" @click="unsubscribe(subscription)">
                                                DELETE
                                            </v-btn>
                                        </td>
                                    </tr>
                                </table>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>
    </v-app>
</div>


<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vuetify/dist/vuetify.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" integrity="sha256-mpnrJ5DpEZZkwkE1ZgkEQQJW/46CSEh/STrZKOB/qoM=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script>
    new Vue({
        el: '#app',
        data: {
            subscriptions: {
                subscriptions: [],
                _links: {}
            },
            email: '',
            searchMinimumYear: '',
            searchModel: '',
            valid: true
        },
        created() {
            axios.get('/api/v1/subscriptions')
                .then((response) => {
                    this.subscriptions = response.data;
                });
        },
        methods: {
            subscribe () {
                if (this.$refs.form.validate()) {
                    axios.post(this.subscriptions._links.self.href, {
                        email: this.email,
                        searchMinimumYear: this.searchMinimumYear,
                        searchModel: this.searchModel
                    })
                        .then((response) => {
                            let data = response.data;

                            if (data.subscription) {
                                this.subscriptions.subscriptions.push(data.subscription)
                            } else if (data.error) {
                                alert("Could not add subscription: " + data.error.message);
                            } else {
                                alert("An unknown error occurred");
                            }
                        });
                }
            },
            unsubscribe (subscription) {
                axios.delete(subscription._links.self.href)
                    .then((response) => {
                        let data = response.data;

                        if (data.error) {
                            alert("Could not delete subscription: " + data.error.message)
                        } else {
                            let index = this.subscriptions.subscriptions.findIndex((_s) => {
                                return _s.subscriptionId === subscription.subscriptionId;
                            });
                            if (index > -1) {
                                this.subscriptions.subscriptions.splice(index, 1);
                            }
                        }
                    })
            }
        }
    })
</script>
</body>
</html>