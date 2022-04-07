const express = require('express')
const favicon = require('serve-favicon')
const path = require('path')

const app = express()

app.set('port', 3000)
app.use(favicon(path.join(__dirname, 'static-node' , 'favicon.ico')))
app.use(express.static('static-node'))

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, "/static-node/templates/index.html"))
})
app.get('/visualizer', (req, res) => {
    res.sendFile(path.join(__dirname, "/static-node/templates/glh_visualize.html"))
})
app.get('/map', (req, res) => {
    res.sendFile(path.join(__dirname, "/static-node/templates/map.html"))
})
app.get('/aggregation', (req, res) => {
    res.sendFile(path.join(__dirname, "/static-node/templates/aggregationOPTICS.html"))
})
app.get('/to_data', (req, res) => {
    res.sendFile(path.join(__dirname, "/static-node/templates/post.html"))
})

app.listen(app.get('port'),  () => {
    console.log("App listening on port " + app.get('port'))
})
