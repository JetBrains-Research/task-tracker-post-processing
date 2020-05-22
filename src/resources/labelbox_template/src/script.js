"use strict";

let toSettedLabels = false;

const labelResult = {
    anonTree: null,
    applyDiffs: null
};

const BAD = 'bad';
const NORMAL = 'normal';
const GOD = 'god';

function checkToSetLabels() {
    toSettedLabels = !(labelResult.anonTree == null || labelResult.applyDiffs == null);
}

function setAnonTreeResult(result) {
    labelResult.anonTree = result;
    checkToSetLabels();
}

function setApplyDiffsResult(result) {
    labelResult.applyDiffs = result;
    checkToSetLabels();
}

function label() {
    if (!toSettedLabels)
        alert('You should label anon tree and apply diffs');
    return;

    const jsonLabel = JSON.stringify(labelResult);
    Labelbox.setLabelForAsset(jsonLabel).then(() => {
        Labelbox.fetchNextAssetToLabel();
    });
}

Labelbox.currentAsset().subscribe((asset) => {
    if (asset) {
        drawItem(asset.data);
    }
});

const defaultConfiguration = {
    classifications: [
        {
            name: "model",
            instructions: "Select the car model",
            type: "radio",
            options: [
                {
                    value: "model_s",
                    label: "Tesla Model S"
                },
                {
                    value: "model_3",
                    label: "Tesla Model 3"
                },
                {
                    value: "model_x",
                    label: "Tesla Model X"
                }
            ]
        },
        {
            name: "image_problems",
            instructions: "Select all that apply",
            type: "checklist",
            options: [
                {
                    value: "blur",
                    label: "Blurry"
                },
                {
                    value: "saturated",
                    label: "Over Saturated"
                },
                {
                    value: "pixelated",
                    label: "Pixelated"
                }
            ]
        },
        {
            name: "description",
            instructions: "Describe this image",
            type: "text"
        }
    ]
};

function drawItem(dataToLabel) {
    const labelForm = `
    <div id="form-image-container">
        <img id="form-image" src="${dataToLabel}"></img>
    </div>
    <div id="quest-cont">
        <div style="margin-right: 50px;">
          <p>Anon tree:</p>
          <button class="form-buttons" onclick="setAnonTreeResult(BAD)">Bad Quality</button>
          <button class="form-buttons" onclick="setAnonTreeResult(NORMAL)">Normal Quality</button>
          <button class="form-buttons" onclick="setAnonTreeResult(GOD)">Good Quality</button>
        </div>
        <div style="margin-left: 50px;">
          <p>Apply diffs:</p>
          <button class="form-buttons" onclick="setApplyDiffsResult(BAD)">Bad Quality</button>
          <button class="form-buttons" onclick="setApplyDiffsResult(NORMAL)">Normal Quality</button>
          <button class="form-buttons" onclick="setApplyDiffsResult(GOD)">Good Quality</button>
        </div>
    </div>
    <div>
        <button class="form-buttons" id="submit-button" onclick="label()">Submit</button>
    </div>
  `;
    document.querySelector('#form').innerHTML = labelForm;
}
