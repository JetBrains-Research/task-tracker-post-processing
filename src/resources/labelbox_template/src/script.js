"use strict";

let toSettedLabels = false;

const labelResult = {
    anonTree: null,
    applyDiffs: null
};

const BAD = 'bad';
const NORMAL = 'normal';
const GOOD = 'good';

const ANON_TREE_QUEST_NAME = 'anonTree';
const APPLY_DIFFS_QUEST_NAME = 'applyDiffs';


// Get img from Labelbox and draw it
Labelbox.currentAsset().subscribe((asset) => {
    if (asset) {
        drawItem(asset.data);
    }
});


// Send answer to Labelbox
function label() {
    getAnonTreeValue();
    getApplyDiffsValue();

    if (!toSettedLabels) {
        alert('You should label anon tree and apply diffs');
        return;
    }

    const jsonLabel = JSON.stringify(labelResult);
    Labelbox.setLabelForAsset(jsonLabel).then(() => {
        Labelbox.fetchNextAssetToLabel();
    });
}


function checkToSetLabels() {
    toSettedLabels = !(labelResult.anonTree == null || labelResult.applyDiffs == null);
}


function getAnonTreeValue() {
    const anonTreeValue = document.querySelector('input[name="' + ANON_TREE_QUEST_NAME + '"]:checked');
    if (anonTreeValue) {
        labelResult.anonTree = anonTreeValue.value;
        checkToSetLabels();
    }
}

function getApplyDiffsValue() {
    const applyDiffsValue = document.querySelector('input[name="' + APPLY_DIFFS_QUEST_NAME + '"]:checked');
    if (applyDiffsValue) {
        labelResult.applyDiffs = applyDiffsValue.value;
        checkToSetLabels();
    }
}


function drawItem(dataToLabel) {
    const labelForm = `
    <div id="form-image-container">
        <img id="form-image" src="${dataToLabel}"></img>
    </div>
    <div id="quest-cont">
        <div id="anonTreeQuest">
          <p>Anon tree (bla bla bla):</p>
          <input type="radio" id="anonBad" name="${ANON_TREE_QUEST_NAME}" value="${BAD}">
          <label for="anonBad">${BAD}</label><br>
          <input type="radio" id="anonNormal" name="${ANON_TREE_QUEST_NAME}" value="${NORMAL}">
          <label for="anonNormal">${NORMAL}</label><br>
          <input type="radio" id="anonGood" name="${ANON_TREE_QUEST_NAME}" value="${GOOD}">
          <label for="anonGood">${GOOD}</label>
        </div>
        <div>
          <p>Apply diffs (bla bla bla):</p>
          <input type="radio" id="diffsBad" name="${APPLY_DIFFS_QUEST_NAME}" value="${BAD}">
          <label for="diffsBad">${BAD}</label><br>
          <input type="radio" id="diffsNormal" name="${APPLY_DIFFS_QUEST_NAME}" value="${NORMAL}">
          <label for="diffsNormal">${NORMAL}</label><br>
          <input type="radio" id="diffsGood" name="${APPLY_DIFFS_QUEST_NAME}" value="${GOOD}">
          <label for="diffsGood">${GOOD}</label>
        </div>
    </div>
    <div>
        <button class="form-buttons" id="submit-button" onclick="label()">Submit</button>
    </div>
  `;
    document.querySelector('#form').innerHTML = labelForm;
}
