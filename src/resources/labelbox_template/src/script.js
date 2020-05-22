"use strict";

let toSettedLabels = false;

const labelResult = {
    anonTree: null,
    applyDiffs: null,
    age: null,
    experience: null
};

const BAD = 'bad';
const NORMAL = 'normal';
const GOOD = 'good';

const ANON_TREE_QUEST_NAME = 'anonTree';
const APPLY_DIFFS_QUEST_NAME = 'applyDiffs';
const EXPERIENCE = 'experience';

const LESS_THAN_HALF_YEAR = 'LESS_THAN_HALF_YEAR';
const FROM_HALF_TO_ONE_YEAR = 'FROM_HALF_TO_ONE_YEAR';
const FROM_ONE_TO_TWO_YEARS = 'FROM_ONE_TO_TWO_YEARS';
const FROM_TWO_TO_FOUR_YEARS = 'FROM_TWO_TO_FOUR_YEARS';
const FROM_FOUR_TO_SIX_YEARS = 'FROM_FOUR_TO_SIX_YEARS';
const MORE_THAN_SIX = 'MORE_THAN_SIX';

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

    getAgeValue();
    getExperienceValue();

    const jsonLabel = JSON.stringify(labelResult);
    console.log(jsonLabel);
    Labelbox.setLabelForAsset(jsonLabel).then(() => {
        clearRadioButton(ANON_TREE_QUEST_NAME);
        clearRadioButton(APPLY_DIFFS_QUEST_NAME);
        clearLabelResult();
        Labelbox.fetchNextAssetToLabel();
    });
}


function clearLabelResult() {
    labelResult.applyDiffs = null;
    labelResult.anonTree = null;
    checkToSetLabels();
}


function clearRadioButton(inputName) {
    const element = document.querySelector('input[name="' + inputName + '"]:checked');
    if (!element) {
        return;
    }
    document.getElementById(element.id).checked = false;

}


function checkToSetLabels() {
    toSettedLabels = !(labelResult.anonTree == null || labelResult.applyDiffs == null);
}


function getAgeValue() {
    const ageValue = document.getElementById("ageInput");
    if (ageValue) {
        labelResult.age = ageValue.value;
    }
}

function setAgeValue() {
    if (labelResult.age) {
        const element = document.getElementById("ageInput");
        element.value = labelResult.age;
    }
}


function setExperienceValue() {
    if (labelResult.experience) {
        const element = document.getElementById(labelResult.experience);
        element.checked = true;
    }
}


function getExperienceValue() {
    const experienceValue = document.querySelector('input[name="' + EXPERIENCE + '"]:checked');
    if (experienceValue) {
        labelResult.experience = experienceValue.value;
    }
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


String.prototype.replaceAll = function(search, replace){
    return this.split(search).join(replace);
};


function getReadableExperience(experience) {
    const lowerExperience = experience.replaceAll('_', ' ').toLowerCase();
    return lowerExperience.charAt(0).toUpperCase() + lowerExperience.slice(1)
}


function drawItem(dataToLabel) {
    const labelForm = `
    <div id="form-meta-info">
        <div id="ageQuest">
            <label for="ageInput">Please, input your age:</label>
            <input type="number" id="ageInput" name="age"
               min="10" max="100">
        </div>
        
        <div>
            <p>Please, set your experience:</p>
            <input type="radio" id="${LESS_THAN_HALF_YEAR}" name="${EXPERIENCE}" value="${LESS_THAN_HALF_YEAR}">
            <label for="${LESS_THAN_HALF_YEAR}">${getReadableExperience(LESS_THAN_HALF_YEAR)}</label><br>
            <input type="radio" id="${FROM_HALF_TO_ONE_YEAR}" name="${EXPERIENCE}" value="${FROM_HALF_TO_ONE_YEAR}">
            <label for="${FROM_HALF_TO_ONE_YEAR}">${getReadableExperience(FROM_HALF_TO_ONE_YEAR)}</label><br>
            <input type="radio" id="${FROM_ONE_TO_TWO_YEARS}" name="${EXPERIENCE}" value="${FROM_ONE_TO_TWO_YEARS}">
            <label for="${FROM_ONE_TO_TWO_YEARS}">${getReadableExperience(FROM_ONE_TO_TWO_YEARS)}</label><br>
            <input type="radio" id="${FROM_TWO_TO_FOUR_YEARS}" name="${EXPERIENCE}" value="${FROM_TWO_TO_FOUR_YEARS}">
            <label for="${FROM_TWO_TO_FOUR_YEARS}">${getReadableExperience(FROM_TWO_TO_FOUR_YEARS)}</label><br>
            <input type="radio" id="${FROM_FOUR_TO_SIX_YEARS}" name="${EXPERIENCE}" value="${FROM_FOUR_TO_SIX_YEARS}">
            <label for="${FROM_FOUR_TO_SIX_YEARS}">${getReadableExperience(FROM_FOUR_TO_SIX_YEARS)}</label><br>
            <input type="radio" id="${MORE_THAN_SIX}" name="${EXPERIENCE}" value="${MORE_THAN_SIX}">
            <label for="${MORE_THAN_SIX}">${getReadableExperience(MORE_THAN_SIX)}</label><br>
        </div>
         
    </div>
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
        <div id="applyDiffsQuest">
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

    setAgeValue();
    setExperienceValue();
}
