var wavesurfer; // eslint-disable-line no-var
/* global WaveSurfer */
/* global localforage */
/* global bootstrap */
/* global JSONEditor */

const key_audio = "key_audio_0";
const key_meta = "key_meta_0";
const item_name_annotation = "annotation";
const item_name_meta = "meta";
const key_annotation_item_names = "key_annotation_item_names";
const default_annotation_item_names = [
    "text",
];

function hms(sec) {
    const timeH = Math.floor((sec % (24 * 60 * 60)) / (60 * 60))
        .toString()
        .padStart(2, "0");
    const timeM = Math.floor(((sec % (24 * 60 * 60)) % (60 * 60)) / 60)
        .toString()
        .padStart(2, "0");
    const timeS = (((sec % (24 * 60 * 60)) % (60 * 60)) % 60)
        .toFixed(0)
        .toString()
        .padStart(2, "0");
    return `${timeH}:${timeM}:${timeS}`;
}

// function load_audio(file) {
//     if (file === null) {
//         return;
//     }
//     {
//         document.getElementById("title").innerText = `${file.name}`;
//         document.title = `${file.name} - Hachiue`;
//     }
//
//     const url_file = URL.createObjectURL(file);
//     const slider = document.querySelector("#slider");
//     slider.oninput = function () {
//         const zoomLevel = Number(slider.value);
//         wavesurfer.zoom(zoomLevel);
//     };
//     wavesurfer.load(url_file);
// }

var regionCreated = false;

function init_wavesurfer() {
    {
        wavesurfer = WaveSurfer.create({
            container: "#waveform",
            waveColor: '#b5b5b5',
            height: 300,
            pixelRatio: 1,
            // minPxPerSec: 15,
            skipLength: 0.5,
            scrollParent: true,
            normalize: true,
            minimap: true,
            backend: "WebAudio",
            cursorColor: "red",
            // barWidth: 3,
            // barMinHeight: 2,
            // barHeight: 2,
            responsive: true,
            plugins: [
                WaveSurfer.cursor.create({
                    showTime: true,
                    opacity: 1,
                    customShowTimeStyle: {
                        'background-color': '#000',
                        color: '#fff',
                        padding: '2px',
                        'font-size': '10px'
                    }
                }),
                WaveSurfer.regions.create(),
                WaveSurfer.minimap.create({
                    height: 30,
                    waveColor: "#ddd",
                    progressColor: "#999",
                }),
                WaveSurfer.timeline.create({
                    container: "#wave-timeline",
                    cursorColor: "purple",
                }),
            ],
        });

        // Load Audio File From Database
        wavesurfer.load(AUDIO_FILE);

        function set_current_time() {
            const currentTime = wavesurfer.getCurrentTime();
            document.getElementById("time-current").innerText =
                currentTime.toFixed(1);
            document.getElementById("time-current-hms").innerText = hms(currentTime);
        }

        wavesurfer.on("seek", function () {
            set_current_time();
        });

        wavesurfer.on("audioprocess", function () {
            if (wavesurfer.isPlaying()) {
                set_current_time();
            }
        });

        localforage.getItem(key_annotation, (err, data_annotation) => {
            if (data_annotation === null) {
                // If Localforage is empty, load from STT.
                loadAnnotationData();
                return;
            }
            loadRegions(data_annotation);
        });
    }

    {
        // Regions
        wavesurfer.on("ready", function () {
            const totalTime = wavesurfer.getDuration();
            document.getElementById("time-total").innerText = `${totalTime.toFixed(
                1
            )}`;
            document.getElementById("time-total-hms").innerText = hms(totalTime);
        });

        wavesurfer.on("region-mouseenter", (region) => {
            old_region = region;
        });

        wavesurfer.on("region-mouseleave", (region) => {
            old_region = null;
        });

        wavesurfer.on("region-click", (region) => {
            current_region = region;
            setRegionActive(region.id);
        });

        wavesurfer.on("region-play", function (region) {
            wavesurfer.play(region.start, region.end);
        });
    }

    {
        // play

        let playButton = document.querySelector("#play");
        let pauseButton = document.querySelector("#pause");
        wavesurfer.on("play", function () {
            playButton.style.display = "none";
            pauseButton.style.display = "";
        });
        wavesurfer.on("pause", function () {
            playButton.style.display = "";
            pauseButton.style.display = "none";
        });
    }

    {
        // Zoom slider
        let slider = document.querySelector("#slider");

        slider.value = wavesurfer.params.minPxPerSec;
        slider.min = wavesurfer.params.minPxPerSec;
        // Allow extreme zoom-in, to see individual samples
        slider.max = 1000;

        slider.addEventListener("input", function () {
            wavesurfer.zoom(Number(this.value));
        });

        // set initial zoom to match slider value
        wavesurfer.zoom(slider.value);
    }

    {
        // Volume
        const volumeInput = document.querySelector("#volume");
        const onChangeVolume = function (e) {
            wavesurfer.setVolume(e.target.value);
        };
        volumeInput.addEventListener("input", onChangeVolume);
        volumeInput.addEventListener("change", onChangeVolume);

        document.getElementById("volume_zero").addEventListener("click", () => {
            wavesurfer.setVolume(0);
            volumeInput.value = 0;
        });
        document.getElementById("volume_max").addEventListener("click", () => {
            wavesurfer.setVolume(1);
            volumeInput.value = 1;
        });
    }
}

function playRegion(region, e) {
    e.stopPropagation();
    // Play on click, loop on shift click
    e.shiftKey ? region.playLoop() : region.play();
}

function loadSTTRegions() {
    var stt_data = JSON.parse(JSON.stringify(STT_DATA.stt_predictions_annotations));
    stt_data.forEach(function (region) {
        region.color = "rgba(0,0,0,0.15)";
        region.drag = false;
        region.resize = false;
        region.id = "stt_" + region.id
        wavesurfer.addRegion(region);
        addTextToSTTRegion(region);
    });
}

// Load Data from Database if localforage is not available.
function loadAnnotationData() {
    if (Object.keys(ANNOTATED_DATA).length < 1) return false;
    loadRegions(ANNOTATED_DATA);
}

const escape_html_map = {
    "&": "&amp;",
    '"': "&quot;",
    "<": "&lt;",
    ">": "&gt;",
};


function setRegionActive(region_id) {
    var region = wavesurfer.regions.list[region_id];
    if (document.querySelectorAll('.active-region').length > 0)
        document.querySelector('.active-region').classList.remove("active-region");
    if (document.querySelectorAll('.active-region-list').length > 0)
        document.querySelector('.active-region-list').classList.remove("active-region-list");
    region.element.classList.add("active-region");
    if (!region_id.includes("stt")) {
        document.querySelector(`.region[data-region_id="${region_id}"]`).classList.add("active-region-list");
    }
}

function setRegionInactive(region_id) {
    var region = wavesurfer.regions.list[region_id];
    region.element.classList.remove("active-region");
    if (!region_id.includes("stt")) {
        document.querySelector(`.region[data-region_id="${region_id}"]`).classList.remove("active-region-list");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    localforage.getItem(
        key_annotation_item_names,
        (err, annotation_item_names) => {
            if (annotation_item_names === null) {
                annotation_item_names = default_annotation_item_names;
                localforage.setItem(
                    key_annotation_item_names,
                    annotation_item_names,
                    () => {
                    }
                );
            }
        }
    );

    init_wavesurfer();

    // document.getElementById("download_button").addEventListener("click", () => {
    //     const dd = new Date();
    //     const YYYY = dd.getFullYear();
    //     const MM = (dd.getMonth() + 1).toString().padStart(2, "0");
    //     const DD = dd.getDate().toString().padStart(2, "0");
    //     const hh = dd.getHours().toString().padStart(2, "0");
    //     const mm = dd.getMinutes().toString().padStart(2, "0");
    //     const ss = dd.getSeconds().toString().padStart(2, "0");
    //     const date_str = `${YYYY}-${MM}-${DD}-${hh}_${mm}_${ss}`;
    //
    //     const name = `annotations_${date_str}.json`;
    //
    //     localforage.getItem(key_annotation, (err, data_annotation) => {
    //         data_annotation.sort((a, b) => {
    //             if (a.start < b.start) {
    //                 return -1;
    //             }
    //             return 1;
    //         });
    //
    //         localforage.getItem(key_meta, (err, data_meta) => {
    //             if (data_meta === null) {
    //                 data_meta = {};
    //             }
    //
    //             const out_data = {};
    //             out_data[item_name_annotation] = data_annotation;
    //             out_data[item_name_meta] = data_meta;
    //
    //             const out = JSON.stringify(out_data, undefined, 4) + "\n";
    //             const url = URL.createObjectURL(
    //                 new Blob([out], {
    //                     type: "application/json",
    //                 })
    //             );
    //             const a = document.createElement("a");
    //             document.body.appendChild(a);
    //             a.download = name;
    //             a.href = url;
    //             a.click();
    //             a.remove();
    //         });
    //     });
    // });

    document.addEventListener("keydown", (e) => {
        if (!e.shiftKey) {
            return;
        }
        switch (e.keyCode) {
            case 32: // space
                wavesurfer.playPause();
                e.preventDefault();
                break;
            case 37: // left
                wavesurfer.skipBackward();
                e.preventDefault();
                break;
            case 39: // right
                wavesurfer.skipForward();
                e.preventDefault();
                break;
            default:
                break;
        }
    });
    document.getElementById("button_play").addEventListener("click", () => {
        wavesurfer.playPause();
    });
});

function changePlaybackRate(elem) {
    wavesurfer.setPlaybackRate(elem.value);
}

function createRegionsCallBack(region) {
    console.log('here', region)
}

function loadRegions(regions) {
    new Promise((resolve, reject) => {
            regions.forEach(function (region) {
                region.color = "rgb(255, 242, 204, 0.2)";
                region.drag = false;
                region.resize = false;
                wavesurfer.addRegion(region);
                addRegionList(region);
                addTextToAnnotationRegion(region);
            });
            resolve('success');
        }
    ).then((value) => {
        document.getElementById('region-count').innerText = regions.length;
    });
}

function randomColor(alpha) {
    return (
        "rgba(" +
        [
            ~~(Math.random() * 255),
            ~~(Math.random() * 255),
            ~~(Math.random() * 255),
            alpha || 1,
        ] +
        ")"
    );
}

function defaultColor(alpha) {
    return (
        "rgba(" +
        [
            255,
            242,
            208,
            alpha || 1,
        ] +
        ")"
    );
}

var old_region = null;
var current_region = null;

function extractRegions(peaks, duration, unit_second) {
    const minValue = 0.005;
    const max_interval = 50;

    const sound_on_indices = [];
    for (let j = 0; j < peaks.length / 2; j++) {
        if (Math.abs(peaks[j * 2 + 1]) >= minValue) {
            sound_on_indices.push(j);
        }
    }

    const spans = [];
    sound_on_indices.forEach(function (val) {
        if (spans.length == 0 || val - spans[spans.length - 1].end > max_interval) {
            spans.push({
                start: val,
                end: val + 1,
            });
        } else {
            spans[spans.length - 1].end = val;
        }
    });

    return spans.map(function (reg) {
        return {
            start: Math.round(reg.start * unit_second * 100) / 100,
            end: Math.round(reg.end * unit_second * 100) / 100,
        };
    });
}

function addRegionList(region) {
    let regionElem = document.createElement('div');
    regionElem.className = 'region';
    regionElem.dataset.region_id = region.id;
    let region_innerHTMl = `
        <span class="serial-num badge rounded-pill bg-secondary"></span>
        <span> <i class="fa fa-microphone-alt" aria-hidden="true"></i></span>
        <div class="audio-range-parent">
            <div>Audio</div>
            <div class="audio-range">
                <span class="start">${hms(region.start)}</span>-<span class="end">${hms(region.end)}</span>
            </div>
        </div>
    `;
    regionElem.innerHTML = region_innerHTMl;
    document.getElementById('region-list').appendChild(regionElem);

    regionElem.addEventListener("click", function (e) {
        // document.querySelector(`.wavesurfer-region[data-id="${region.id}"]`).click();
        playRegion(wavesurfer.regions.list[region.id], e);
    });
}

function emptyResults() {
    var elem = document.querySelector('.result-section .result');
    elem.innerHTML = `
        <div class="audio-details">
            No Region Selected.
        </div>
        <div class="audio-data">

        </div>
    `;
}

function addTextToSTTRegion(region) {
    if (!region.id.includes('stt')) return false;
    var regionText = document.createElement('div');
    regionText.className = "region-stt-text";
    regionText.innerHTML = ("text" in region.data) ? region.data.text == '' ? '' : region.data.text : '';
    document.querySelector(`[data-id=${region.id}]`).appendChild(regionText);
}

function addTextToAnnotationRegion(region) {
    if (region.id.includes('stt')) return false;
    var regionText = document.createElement('div');
    regionText.className = "region-text";
    regionText.innerHTML = ("text" in region.data) ? region.data.text == '' ? '' : region.data.text : '';
    document.querySelector(`[data-id=${region.id}]`).appendChild(regionText);
}

function sortRegions(value, order = 1) {
    return value.sort((a, b) => {
        return a.start - b.start;
    });
}

function sortRegionList() {
    localforage.getItem(key_annotation).then(function (value) {
        // This code runs once the value has been loaded
        // from the offline store.
        var sorted = sortRegions(value, 1);
        clearRegionList();
        sorted.forEach(function (region) {
            addRegionList(region);
        });
        localforage.setItem(key_annotation, sorted, () => {}
        );
        document.getElementById('region-count').innerText = sorted.length;
    }).catch(function (err) {
        // This code runs if there were any errors
        console.log(err);
    });
}

function clearRegionList() {
    document.getElementById('region-list').innerHTML = "";
}

// Check if region is overlaps
function validateRegion(region) {
    var overlap = false;
    var value = wavesurfer.regions.list;
    Object.keys(value).filter((key) => !key.includes('stt_')).reduce(function (r, e) {
        // Overlap condition
        // If region right end is inside value and left is not overllaped.
        var leftCondition = (value[e].start > region.start && value[e].start < region.end);
        // If region left end is inside value and right is outside.
        var rightCondition = (value[e].end > region.start && value[e].end < region.end);
        // if engulfed.
        var midCondition = (value[e].start < region.start && value[e].end > region.end);
        if (leftCondition || rightCondition || midCondition) {
            overlap = true;
            return;
        }
        return r;
    }, {})

    return overlap ? false : true;
}


function splitRegion(region) {
    var current_time = wavesurfer.getCurrentTime();
    deleteRegion(region.id);
    localforage.getItem(key_annotation, (err, data) => {
        var region_data = data.filter(i => i.id == region.id);

        old_end = region_data[0].end;

        region_data[0].data = {};

        // First Region
        region_data[0].id = region_data[0].id + "split_1";
        region_data[0].end = current_time - 0.05;
        loadRegions(region_data);

        // Second Region
        region_data[0].id = region_data[0].id + "split_2";
        region_data[0].start = current_time + 0.05;
        region_data[0].end = old_end;
        loadRegions(region_data);
    });
}

// Direction 1 is right, -1 is left
function mergeRegion(region, direction = 1) {
    localforage.getItem(key_annotation, (err, data) => {
        var region_data = data.filter(i => i.id == region.id);
        var cursorIdx = data.map(e => e.id).indexOf(region.id);
        var toBeMergedRegion = direction > 0 ? data[cursorIdx + 1] : data[cursorIdx - 1];

        var cursorRegion = data[cursorIdx];


        // deleteRegion(toBeMergedRegion.id);
        // deleteRegion(cursorRegion.id);

        // Delete Region Function is not used as not to save the same data again and again.
        // Saving Data will be done after merging only.
        wavesurfer.regions.list[toBeMergedRegion.id].remove();
        wavesurfer.regions.list[cursorRegion.id].remove();

        var merged_text = null;
        if ('text' in cursorRegion.data || 'text' in toBeMergedRegion.data) {
            var cursorText = 'text' in cursorRegion.data ? cursorRegion.data.text : "";
            var mergeText = 'text' in toBeMergedRegion.data ? toBeMergedRegion.data.text : "";
            merged_text = [cursorText + " " + mergeText]
        }

        var cursorLabel = 'labels' in cursorRegion.data ? cursorRegion.data.labels : [];
        var mergeLabel = 'labels' in toBeMergedRegion.data ? toBeMergedRegion.data.labels : [];

        if (direction > 0) {
            region_data[0].end = toBeMergedRegion.end;
            region_data[0].data['text'] = merged_text;
            region_data[0].data['labels'] = [...new Set([...cursorLabel, ...mergeLabel])];
        } else {
            region_data[0].start = toBeMergedRegion.start;
            region_data[0].data['text'] = toBeMergedRegion.data['text'] + " " + cursorRegion.data['text'];
            region_data[0].data['labels'] = [...new Set([...mergeLabel, ...cursorLabel])];
        }
        loadRegions(region_data);

    });
}