<template lang="pug">
    row.home-container(align-v='top' align-h="left" position="relative" width='fit-content' min-width="100vw" height="100vh" overflow="hidden" :class="{labelSelected: !!$root.selectedLabel}")
        LabelPicker
        
        column.home-container(name="home-container" :visibility="$root.selectedLabel? 'visible' : 'hidden'" align-v="top" flex-grow="1" height="100vh" overflow="auto")
            CenterStage
        
        VideoPicker
            
                
</template>
<script>
const { dynamicSort, logBlock, checkIf, get, set } = require("good-js")
let Fuse = require("fuse.js").default

// 
// summary
//
    // set:
    //     this.$root.selectedVideo
    //     this.$root.selectedLabel
    //     this.$root.videos
    // 
    // get:
    //     this.$root.labels
    //     this.$root.segments
    // 
    // retreives:
    // 
    // listeners:
    //     this.$root.$watch("labels")
    // 
    // emits:
    // 

export default {
    name: "HomePage",
    components: {
        CenterStage: require("../organisms/CenterStage").default,
        VideoPicker: require("../organisms/VideoPicker").default,
        LabelPicker: require("../organisms/LabelPicker").default,
    },
    methods: {}
}
</script>
<style lang="sass">

.home-container
    .nub
        --nub-size: 7rem
        font-size: 15pt
    
.rounded-search
    width: 25rem
    max-width: 85%
    margin: 1.2rem
    padding: 0.7rem 2rem 1rem
    background-color: white
    border-radius: 2rem
    height: fit-content
    box-shadow: var(--shadow-1)
    
</style>