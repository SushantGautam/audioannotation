var wavesurfer; // eslint-disable-line no-var
/* global WaveSurfer */
/* global localforage */
/* global bootstrap */
/* global JSONEditor */

const key_audio = "key_audio_0";
const key_annotation = "key_annotation_0";
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

function load_audio(file) {
    if (file === null) {
        return;
    }
    {
        document.getElementById("title").innerText = `${file.name}`;
        document.title = `${file.name} - Hachiue`;
    }

    const url_file = URL.createObjectURL(file);
    const slider = document.querySelector("#slider");
    slider.oninput = function () {
        const zoomLevel = Number(slider.value);
        wavesurfer.zoom(zoomLevel);
    };
    wavesurfer.load(url_file);
}

function load_files(files) {
    Array.from(files).forEach((f) => {
        if (f.type.match(/audio\/*/)) {
            /**/
            load_audio(f);

            localforage.setItem(key_audio, f).catch((err) => {
                alert(err);
            });
        } else if (f.type == "application/json") {
            wavesurfer.clearRegions();

            const reader = new FileReader();
            reader.onload = () => {
                try {
                    const d = JSON.parse(reader.result);
                    console.log(item_name_annotation, d[item_name_annotation])
                    loadRegions(d[item_name_annotation]);

                    //meta
                    localforage
                        .setItem(key_meta, d[item_name_meta], () => {
                            // on success
                        })
                        .catch((err) => {
                            alert(`Error on save: ${err}`);
                        });
                } catch (error) {
                    alert(error);
                }
                saveRegions();
            };
            reader.readAsText(f);
        } else {
            alert(`Unsupported file type ${f.type}`);
        }
    });
}


function init_wavesurfer() {
     var stt_data = JSON.parse(JSON.stringify(STT_DATA.stt_predictions_annotations));
    stt_data.forEach(function (region) {
        region.drag = false;
        region.resize = false;
        // region.attributes= {
        //     label: region.data.text,
        // }
    });
    {
        wavesurfer = WaveSurfer.create({
            container: "#waveform",
            height: 300,
            pixelRatio: 1,
            skipLength: 0.5,
            scrollParent: true,
            normalize: true,
            minimap: true,
            backend: "MediaElement",
            cursorColor: "red",
            plugins: [
                WaveSurfer.regions.create({
                    regions: stt_data,
                }),
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
                loadSTTData();
                return;
            }
            loadRegions(data_annotation);
        });

        localforage.getItem(key_audio, (err, data_audio) => {
            load_audio(data_audio);
        });
    }

    {
        // Regions

        wavesurfer.on("ready", function () {
            wavesurfer.enableDragSelection({
                color: randomColor(0.1),
            });

            const totalTime = wavesurfer.getDuration();
            document.getElementById("time-total").innerText = `${totalTime.toFixed(
                1
            )}`;
            document.getElementById("time-total-hms").innerText = hms(totalTime);
        });
        wavesurfer.on("region-click", function (region, e) {
            e.stopPropagation();
            // Play on click, loop on shift click
            e.shiftKey ? region.playLoop() : region.play();
        });
        wavesurfer.on("region-click", editAnnotation);
        wavesurfer.on("region-click", (region) => {loadResults(region);});
        wavesurfer.on("region-created", function (region) {
            appendDeleteIcon(region.id);
        });
        wavesurfer.on("region-updated", saveRegions);
        wavesurfer.on("region-removed", saveRegions);

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

        document
            .querySelector('[data-action="delete-region"]')
            .addEventListener("click", function () {
                deleteRegionFunc();
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

    {
        ["start", "end"].forEach((label) => {
            document.getElementById(label).addEventListener("change", (e) => {
                document.getElementById(`${label}-hms`).value = hms(e.target.value);
            });
            document
                .getElementById(`${label}-setnow`)
                .addEventListener("click", (e) => {
                    document.getElementById(`${label}`).value =
                        document.getElementById(`time-current`).innerText;
                });
        });
    }

    {
        // UI
        // document.getElementById("title").innerText = "Hachiue";
        // document.title = "Hachiue";
        document.getElementById("time-total").innerText = "0.00";
        document.getElementById("time-current").innerText = "0.00";
        document.getElementById("time-total-hms").innerText = "00:00:00";
        document.getElementById("time-current-hms").innerText = "00:00:00";
        const form = document.forms.edit;
        form.style.opacity = 0;
    }
}

// Load Data from STT Naver if localforage is not available.
function loadSTTData() {
    if (Object.keys(STT_DATA).length < 1) return;
    loadRegions(STT_DATA.stt_predictions_annotations);
}

function deleteRegionFunc() {
    let form = document.forms.edit;
    let regionId = form.dataset.region;
    if (regionId) {
        wavesurfer.regions.list[regionId].remove();
        form.reset();
    }
}

function appendDeleteIcon(elem) {
    let btnHTML = document.createElement('button');
    btnHTML.className = 'btn btn-sm delete-range';
    btnHTML.setAttribute('data-action', 'delete-region');
    btnHTML.innerHTML = "x";
    btnHTML.addEventListener("click", function () {
        btnHTML.closest('.wavesurfer-region').click();
        deleteRegionFunc();
    });
    document.querySelector(`[data-id=${elem}]`).appendChild(btnHTML);
}

function clear_annotations() {
    localforage
        .removeItem(key_annotation, () => {
        })
        .catch((err) => {
            alert(err);
        });

    wavesurfer.clearRegions();
    old_region = null;
}

const escape_html_map = {
    "&": "&amp;",
    '"': "&quot;",
    "<": "&lt;",
    ">": "&gt;",
};

function set_annotation_items(annotation_item_names) {
    const area = document.getElementById("annotation_item_area");
    area.innerHTML = "";

    let row_idx = 0;
    for (let j = 0; j < annotation_item_names.length; ++j) {
        const item_name = annotation_item_names[j].replace(
            /[&"<>]/g,
            (e) => escape_html_map[e]
        );

        if (j % 2 == 0) {
            area.innerHTML += `<div class="form-group row" id="annotation_item_row_${row_idx}">
                <div class="col" id="annotation_item_${j}">
                </div>
                <div class="col" id="annotation_item_${j + 1}">
                </div>
            </div>`;
            row_idx += 1;
        }
        const row = document.getElementById(`annotation_item_${j}`);
        var final_name = item_name;

        row.innerHTML = `
                <div class="col">
                    <label for="vals__${final_name}">${item_name}</label>
                    <textarea id="vals__${final_name}" class="form-control" name="vals__${final_name}"></textarea>
                </div>
        `;
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
            set_annotation_items(annotation_item_names);
        }
    );

    init_wavesurfer();

    {
        // Reset
        const resetButton = document.querySelector("#reset");
        resetButton.addEventListener("click", () => {
            if (!confirm("Clear all?")) {
                return;
            }

            clear_annotations();

            localforage
                .removeItem(key_audio, () => {
                })
                .catch((err) => {
                    alert(err);
                });

            wavesurfer.empty();
            wavesurfer.destroy();
            init_wavesurfer();
        });
    }


    document.getElementById("download_button").addEventListener("click", () => {
        const dd = new Date();
        const YYYY = dd.getFullYear();
        const MM = (dd.getMonth() + 1).toString().padStart(2, "0");
        const DD = dd.getDate().toString().padStart(2, "0");
        const hh = dd.getHours().toString().padStart(2, "0");
        const mm = dd.getMinutes().toString().padStart(2, "0");
        const ss = dd.getSeconds().toString().padStart(2, "0");
        const date_str = `${YYYY}-${MM}-${DD}-${hh}_${mm}_${ss}`;

        const name = `annotations_${date_str}.json`;

        localforage.getItem(key_annotation, (err, data_annotation) => {
            data_annotation.sort((a, b) => {
                if (a.start < b.start) {
                    return -1;
                }
                return 1;
            });

            localforage.getItem(key_meta, (err, data_meta) => {
                if (data_meta === null) {
                    data_meta = {};
                }

                const out_data = {};
                out_data[item_name_annotation] = data_annotation;
                out_data[item_name_meta] = data_meta;

                const out = JSON.stringify(out_data, undefined, 4) + "\n";
                const url = URL.createObjectURL(
                    new Blob([out], {
                        type: "application/json",
                    })
                );
                const a = document.createElement("a");
                document.body.appendChild(a);
                a.download = name;
                a.href = url;
                a.click();
                a.remove();
            });
        });
    });

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

function createRegionsCallBack(region) {
    console.log('here', region)
}

function saveRegions() {
    const mydata = Object.keys(wavesurfer.regions.list).map(function (id) {
        const region = wavesurfer.regions.list[id];
        return {
            id: region.id,
            user: USER_ID,
            start: region.start,
            end: region.end,
            updated_date: new Date().toISOString(),
            data: region.data,
        };
    });

    localforage
        .setItem(key_annotation, mydata, () => {
            // on success
        })
        .catch((err) => {
            alert(`Error on save: ${err}`);
        });
}

function loadRegions(regions) {
    regions.forEach(function (region) {
        region.color = randomColor(0.1);
        wavesurfer.addRegion(region);
        addRegionList(region);
        var regionText = document.createElement('div');
        regionText.className = "region-stt-text";
        regionText.innerHTML = ("text" in region.data) ? region.data.text == '' ? '' : region.data.text : '';
        document.querySelector(`[data-id=${region.id}]`).appendChild(regionText);
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

function save_a_region(region) {
    const form = document.forms.edit;
    const data = {};
    for (const [key, el] of Object.entries(form.elements)) {
        if (key.startsWith("vals__")) {
            let v = el.value;
            if (key != "vals__memo") {
                // Clean blanks and line breaks
                v = v.replace(/^\s+|\s+$|\n/g, "");
            }
            data[key.substr("vals__".length)] = v;
        }
    }

    region.update({
        start: form.elements.start.value,
        end: form.elements.end.value,
        data: data,
    });
    form.style.opacity = 0;
}

var old_region = null;

function editAnnotation(region) {
    if (old_region !== null && region != old_region) {
        save_a_region(old_region);
    }
    old_region = region;

    const form = document.forms.edit;
    form.style.opacity = 1;
    form.elements.start.value = Math.round(region.start * 100) / 100;
    document.getElementById("start").dispatchEvent(new Event("change"));
    form.elements.end.value = Math.round(region.end * 100) / 100;
    document.getElementById("end").dispatchEvent(new Event("change"));

    for (const [key, el] of Object.entries(form.elements)) {
        if (key.startsWith("vals__")) {
            // const mykey = key.substr("vals__".length);
            el.value = region.data['text'] || "";
        }
    }

    form.onsubmit = function (e) {
        e.preventDefault();
        save_a_region(region);
    };
    form.onreset = function () {
        form.style.opacity = 0;
        form.dataset.region = null;
    };
    form.dataset.region = region.id;
}

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

    regionElem.addEventListener("click", function () {
        console.log('here')
        document.querySelector(`.wavesurfer-region[data-id="${region.id}"]`).click();
    });
}

function loadResults(region) {
    var elem = document.querySelector('.result-section > .result');
    elem.innerHTML = `
        <div class="audio-details">
            <span class="serial-num badge rounded-pill bg-dark"></span>
            <span><i class="fas fa-microphone-alt"></i> 
            AudioTitle <span class="start">${hms(region.start)}</span>-<span class="end">${hms(region.end)}</span></span>
        </div>
        <div class="label-parent">
            <label>Label : </label>
            <span class="badge rounded-pill bg-dark">${region.data.labels}</span>
        </div>
        <div class="text-parent">
            <label>Text : </label>
            <span class="text">${region.data.text}</span>
        </div>
    `;
}