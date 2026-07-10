// ============================================================
// СОСТОЯНИЕ
// ============================================================
const state = {
    habits: [],
    currentTab: 'today',
    theme: 'white',
    points: 0,
    level: 1,
    xp: 0,
    xpNeeded: 50,
    streak: 0,
    maxStreak: 0,
    totalCompleted: 0,
    username: 'Пользователь',
    hasSeenOnboarding: false,
    hasSeenWelcome: false,
    completedToday: 0,
    calendarMonth: new Date().getMonth(),
    calendarYear: new Date().getFullYear(),
    hasSubscription: false,
    subscriptionType: null,
    subscriptionStart: null,
    subscriptionEnd: null,
    trialUsed: false,
    // ===== ДЛЯ ФИКСА БАГА: запоминаем, за какой день уже дали XP =====
    lastXpDate: null,
    xpGivenToday: false
};

// ============================================================
// ПОДПИСКА
// ============================================================
const PRICES = {
    trial: { days: 3, price: 0, label: 'Пробный (3 дня)', habits: 15 },
    basic: { days: 30, price: 61, label: 'Обычная (30 дней)', habits: 15 },
    premium: { days: 30, price: 122, label: 'Премиум (30 дней)', habits: 50 }
};

// ============================================================
// 50 ДОСТИЖЕНИЙ
// ============================================================
const achievementsList = [
    { id: 'first', name: 'Первый шаг', desc: 'Добавить первую привычку' },
    { id: 'week_streak', name: 'Неделя дисциплины', desc: 'Серия 7 дней' },
    { id: 'month_streak', name: 'Месяц силы воли', desc: 'Серия 30 дней' },
    { id: 'year_streak', name: 'Год привычек', desc: 'Серия 365 дней' },
    { id: 'hundred', name: 'Сотня', desc: 'Выполнить 100 привычек' },
    { id: 'five_hundred', name: 'Полтысячи', desc: 'Выполнить 500 привычек' },
    { id: 'thousand', name: 'Тысяча', desc: 'Выполнить 1000 привычек' },
    { id: 'level_5', name: 'Новичок', desc: 'Достичь 5 уровня' },
    { id: 'level_10', name: 'Профи', desc: 'Достичь 10 уровня' },
    { id: 'level_25', name: 'Мастер', desc: 'Достичь 25 уровня' },
    { id: 'level_50', name: 'Легенда', desc: 'Достичь 50 уровня' },
    { id: 'level_100', name: 'Миф', desc: 'Достичь 100 уровня' },
    { id: 'habits_5', name: 'Коллекционер', desc: 'Иметь 5 привычек' },
    { id: 'habits_10', name: 'Энтузиаст', desc: 'Иметь 10 привычек' },
    { id: 'habits_20', name: 'Мастер привычек', desc: 'Иметь 20 привычек' },
    { id: 'streak_3', name: 'Первая серия', desc: 'Серия 3 дня' },
    { id: 'streak_14', name: 'Две недели', desc: 'Серия 14 дней' },
    { id: 'streak_60', name: 'Два месяца', desc: 'Серия 60 дней' },
    { id: 'streak_100', name: '100 дней', desc: 'Серия 100 дней' },
    { id: 'points_100', name: 'Копилка', desc: 'Накопить 100 баллов' },
    { id: 'points_500', name: 'Банкир', desc: 'Накопить 500 баллов' },
    { id: 'points_1000', name: 'Миллионер', desc: 'Накопить 1000 баллов' },
    { id: 'morning', name: 'Ранняя пташка', desc: 'Выполнить привычку до 8:00' },
    { id: 'evening', name: 'Совушка', desc: 'Выполнить привычку после 22:00' },
    { id: 'perfect_day', name: 'Идеальный день', desc: 'Выполнить все привычки за день' },
    { id: 'perfect_week', name: 'Идеальная неделя', desc: 'Выполнять все привычки 7 дней' },
    { id: 'perfect_month', name: 'Идеальный месяц', desc: 'Выполнять все привычки 30 дней' },
    { id: 'friend_1', name: 'Первый друг', desc: 'Пригласить первого друга' },
    { id: 'friend_5', name: 'Компания', desc: 'Пригласить 5 друзей' },
    { id: 'friend_10', name: 'Команда', desc: 'Пригласить 10 друзей' },
    { id: 'friend_25', name: 'Армия', desc: 'Пригласить 25 друзей' },
    { id: 'friend_50', name: 'Легенда', desc: 'Пригласить 50 друзей' },
    { id: 'streak_200', name: '200 дней', desc: 'Серия 200 дней' },
    { id: 'streak_365', name: 'Год без остановки', desc: 'Серия 365 дней' },
    { id: 'habits_30', name: 'Массовый подход', desc: 'Иметь 30 привычек' },
    { id: 'habits_50', name: 'Предел совершенства', desc: 'Иметь 50 привычек' },
    { id: 'level_200', name: 'Эксперт', desc: 'Достичь 200 уровня' },
    { id: 'level_500', name: 'Гуру', desc: 'Достичь 500 уровня' },
    { id: 'level_1000', name: 'Легенда', desc: 'Достичь 1000 уровня' },
    { id: 'premium_activate', name: 'Премиум пользователь', desc: 'Активировать премиум-подписку' },
    { id: 'premium_year', name: 'Премиум на год', desc: 'Быть в премиуме 365 дней' },
    { id: 'veteran', name: 'Ветеран', desc: 'Выполнить 5000 привычек' },
    { id: 'morning_week', name: 'Ранняя неделя', desc: 'Выполнять привычки до 8:00 7 дней' },
    { id: 'evening_week', name: 'Совиная неделя', desc: 'Выполнять привычки после 22:00 7 дней' },
    { id: 'perfect_year', name: 'Идеальный год', desc: 'Выполнять все привычки 365 дней' },
    { id: 'no_skip_day', name: 'Без пропусков', desc: 'Выполнять привычки 30 дней без пропусков' },
    { id: 'points_5000', name: 'Магнат', desc: 'Накопить 5000 баллов' },
    { id: 'points_10000', name: 'Олигарх', desc: 'Накопить 10000 баллов' },
    { id: 'habits_all_types', name: 'Разнообразие', desc: 'Иметь привычки всех типов' },
    { id: 'super_veteran', name: 'Супер-ветеран', desc: 'Выполнить 10000 привычек' }
];

// ============================================================
// ЗАГРУЗКА
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    loadState();
    applyTheme(state.theme);

    document.getElementById('loading-screen').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');

    // ===== ПРОВЕРКА ПОДПИСКИ =====
    if (!checkSubscription()) {
        showSubscriptionScreen();
        return;
    }

    document.getElementById('main-interface').classList.remove('hidden');

    setTimeout(function() {
        document.getElementById('logo-animation').classList.add('hidden');
        if (!state.hasSeenWelcome) {
            showWelcome();
        } else if (!state.hasSeenOnboarding) {
            startOnboarding();
        } else {
            initApp();
        }
    }, 5500);

    setupEventListeners();
});

// ============================================================
// ПРОВЕРКА ПОДПИСКИ
// ============================================================
function checkSubscription() {
    if (!state.hasSubscription) return false;
    if (!state.subscriptionEnd) return false;
    var now = new Date();
    var end = new Date(state.subscriptionEnd);
    if (now > end) {
        state.hasSubscription = false;
        state.subscriptionType = null;
        state.subscriptionEnd = null;
        saveState();
        return false;
    }
    return true;
}

function getRemainingDays() {
    if (!state.subscriptionEnd) return 0;
    var now = new Date();
    var end = new Date(state.subscriptionEnd);
    var diff = end - now;
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

function activateSubscription(type) {
    var plan = PRICES[type];
    if (!plan) return;
    var start = new Date();
    var end = new Date();
    end.setDate(end.getDate() + plan.days);
    state.hasSubscription = true;
    state.subscriptionType = type;
    state.subscriptionStart = start.toISOString();
    state.subscriptionEnd = end.toISOString();
    if (type === 'trial') {
        state.trialUsed = true;
    }
    saveState();
    document.getElementById('subscription-screen').classList.add('hidden');
    document.getElementById('main-interface').classList.remove('hidden');
    setTimeout(function() {
        document.getElementById('logo-animation').classList.add('hidden');
        if (!state.hasSeenWelcome) {
            showWelcome();
        } else if (!state.hasSeenOnboarding) {
            startOnboarding();
        } else {
            initApp();
        }
    }, 500);
}

function showSubscriptionScreen() {
    var screen = document.getElementById('subscription-screen');
    if (!screen) return;
    screen.classList.remove('hidden');
    document.getElementById('main-interface').classList.add('hidden');
    document.getElementById('logo-animation').classList.add('hidden');
    updateSubscriptionInfo();
}

function updateSubscriptionInfo() {
    var trialBtn = document.getElementById('sub-trial-btn');
    if (trialBtn) {
        if (state.trialUsed) {
            trialBtn.disabled = true;
            trialBtn.textContent = 'Пробный период использован';
            trialBtn.style.opacity = '0.5';
        } else {
            trialBtn.disabled = false;
            trialBtn.textContent = 'Попробовать 3 дня бесплатно';
            trialBtn.style.opacity = '1';
        }
    }
}

// ============================================================
// ИНИЦИАЛИЗАЦИЯ
// ============================================================
function initApp() {
    renderHabits();
    updateStats();
    renderAchievements();
    renderLeaderboard();
    renderCalendar();
    updateRemainingDays();
}

function updateRemainingDays() {
    var days = getRemainingDays();
    var el = document.getElementById('profile-subscription');
    if (el) {
        if (state.subscriptionType === 'trial') {
            el.textContent = 'Пробный (осталось ' + days + ' дн.)';
        } else if (state.subscriptionType === 'premium') {
            el.textContent = 'Премиум (осталось ' + days + ' дн.)';
        } else if (state.subscriptionType === 'basic') {
            el.textContent = 'Обычная (осталось ' + days + ' дн.)';
        } else {
            el.textContent = 'Нет';
        }
    }
}

// ============================================================
// ХРАНЕНИЕ
// ============================================================
function loadState() {
    try {
        var saved = localStorage.getItem('habitmon_state');
        if (saved) {
            var parsed = JSON.parse(saved);
            for (var key in parsed) {
                state[key] = parsed[key];
            }
        }
    } catch (e) {}
}
function saveState() {
    try {
        localStorage.setItem('habitmon_state', JSON.stringify(state));
    } catch (e) {}
}

function showWelcome() {
    var welcome = document.getElementById('welcome-screen');
    welcome.classList.remove('hidden');
    var hour = new Date().getHours();
    var msg = 'Добро пожаловать в HabitMon';
    if (hour < 12) msg = 'Начни день с привычек';
    else if (hour < 17) msg = 'Продолжай развиваться';
    else msg = 'Отличное время для привычек';
    document.getElementById('welcome-message').textContent = msg;
}

function applyTheme(theme) {
    var themes = ['white', 'blue', 'lavender'];
    document.body.classList.remove('theme-white', 'theme-blue', 'theme-lavender');
    document.body.classList.add('theme-' + theme);
    state.theme = theme;
    saveState();
}

function cycleTheme() {
    var themes = ['white', 'blue', 'lavender'];
    var idx = themes.indexOf(state.theme);
    applyTheme(themes[(idx + 1) % themes.length]);
    showToast('Тема изменена');
}

// ============================================================
// ИНСТРУКЦИЯ
// ============================================================
var onboardingSteps = [
    { title: 'Добавляй привычки', desc: 'Нажми на кнопку "Новая привычка" и создай свою первую.' },
    { title: 'Отмечай выполнение', desc: 'Просто нажми на привычку, когда сделаешь её.' },
    { title: 'Следи за прогрессом', desc: 'Во вкладке "Прогресс" ты увидишь свой уровень и календарь.' },
    { title: 'Достижения', desc: 'Выполняй привычки и открывай новые достижения. Их здесь 50!' },
    { title: 'Друзья и рейтинг', desc: 'Приглашай друзей, соревнуйся с ними и поднимайся в рейтинге.' },
    { title: 'Профиль', desc: 'В профиле ты видишь свои баллы, серию и общую статистику.' }
];
var onboardingStep = 0;

function startOnboarding() {
    document.getElementById('onboarding').classList.remove('hidden');
    showOnboardingStep(0);
}

function showOnboardingStep(step) {
    var data = onboardingSteps[step];
    if (!data) return;
    document.getElementById('onboarding-title').textContent = data.title;
    document.getElementById('onboarding-desc').textContent = data.desc;
    var dots = document.querySelectorAll('.dot');
    for (var i = 0; i < dots.length; i++) {
        dots[i].classList.toggle('active', i === step);
    }
    document.getElementById('onboarding-next').textContent = step === onboardingSteps.length - 1 ? 'Начать' : 'Далее';
    onboardingStep = step;
}

// ============================================================
// ПРИВЫЧКИ С ФИКСОМ БАГА
// ============================================================
function renderHabits() {
    var list = document.getElementById('habits-list');
    var today = new Date().toISOString().split('T')[0];
    if (state.habits.length === 0) {
        list.innerHTML = '<p class="empty-habits">Добавь свою первую привычку</p>';
        return;
    }
    var html = '';
    for (var i = 0; i < state.habits.length; i++) {
        var habit = state.habits[i];
        var log = null;
        if (habit.logs) {
            for (var j = 0; j < habit.logs.length; j++) {
                if (habit.logs[j].date === today) {
                    log = habit.logs[j];
                    break;
                }
            }
        }
        var done = log && log.completed || false;
        html += '<div class="habit-item ' + (done ? 'completed' : '') + '" data-index="' + i + '">';
        html += '<div class="habit-left">';
        html += '<span class="habit-icon">';
        html += '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">';
        html += '<path d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>';
        html += '</svg>';
        html += '</span>';
        html += '<span class="habit-name">' + habit.name + '</span>';
        html += '</div>';
        html += '<div style="display:flex;align-items:center;gap:4px;">';
        html += '<span class="habit-check">' + (done ? '✓' : '○') + '</span>';
        html += '<button class="habit-delete" data-index="' + i + '" title="Удалить">';
        html += '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">';
        html += '<path d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"/>';
        html += '</svg>';
        html += '</button>';
        html += '</div>';
        html += '</div>';
    }
    list.innerHTML = html;

    var items = document.querySelectorAll('.habit-item');
    for (var k = 0; k < items.length; k++) {
        (function(el) {
            var idx = parseInt(el.dataset.index);
            el.addEventListener('click', function(e) {
                if (e.target.closest('.habit-delete')) return;
                toggleHabit(idx);
            });
        })(items[k]);
    }

    var deletes = document.querySelectorAll('.habit-delete');
    for (var m = 0; m < deletes.length; m++) {
        (function(btn) {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                var idx = parseInt(btn.dataset.index);
                if (confirm('Удалить привычку "' + state.habits[idx].name + '"?')) {
                    state.habits.splice(idx, 1);
                    saveState();
                    renderHabits();
                    updateStats();
                    showToast('Привычка удалена');
                }
            });
        })(deletes[m]);
    }
}

// ============================================================
// TOGGLE HABIT С ФИКСОМ БАГА
// ============================================================
function toggleHabit(index) {
    var habit = state.habits[index];
    if (!habit) return;
    var today = new Date().toISOString().split('T')[0];
    if (!habit.logs) habit.logs = [];
    var existing = null;
    for (var i = 0; i < habit.logs.length; i++) {
        if (habit.logs[i].date === today) {
            existing = habit.logs[i];
            break;
        }
    }
    if (existing) {
        // ===== ФИКС БАГА: если привычка уже выполнена сегодня, не даём XP повторно =====
        if (!existing.completed) {
            // Только если переключаем с НЕ ВЫПОЛНЕНО на ВЫПОЛНЕНО
            existing.completed = true;
            addXP(20);
            state.xpGivenToday = true;
        } else {
            // Если уже выполнена — просто снимаем отметку, XP не трогаем
            existing.completed = false;
        }
    } else {
        // Новая запись за сегодня
        habit.logs.push({ date: today, completed: true });
        addXP(20);
        state.xpGivenToday = true;
    }
    saveState();
    renderHabits();
    updateStats();
    checkAchievements();
    renderAchievements();
    renderLeaderboard();
}

// ============================================================
// ДОБАВЛЕНИЕ ПРИВЫЧКИ
// ============================================================
function addHabit(name) {
    if (!name.trim()) { showToast('Введите название'); return; }
    // Определяем лимит привычек в зависимости от подписки
    var maxHabits = 5; // по умолчанию
    if (state.hasSubscription) {
        if (state.subscriptionType === 'premium') {
            maxHabits = 50;
        } else if (state.subscriptionType === 'basic' || state.subscriptionType === 'trial') {
            maxHabits = 15;
        }
    }
    if (state.habits.length >= maxHabits) {
        if (state.subscriptionType === 'premium') {
            showToast('Достигнут лимит привычек (50). Удалите ненужные.');
        } else if (state.subscriptionType === 'basic' || state.subscriptionType === 'trial') {
            showToast('Достигнут лимит привычек (15). Для большего выберите премиум.');
        } else {
            showToast('Доступно 5 привычек. Оформите подписку для большего количества.');
        }
        return;
    }
    state.habits.push({
        id: Date.now(),
        name: name.trim(),
        logs: []
    });
    saveState();
    renderHabits();
    updateStats();
    checkAchievements();
    renderAchievements();
    renderLeaderboard();
    showToast('Привычка "' + name + '" добавлена');
}

// ============================================================
// XP И УРОВЕНЬ
// ============================================================
function addXP(amount) {
    // ===== ФИКС БАГА: не даём XP дважды за один день =====
    var today = new Date().toISOString().split('T')[0];
    if (state.xpGivenToday) {
        // Если XP уже давали сегодня — пропускаем
        return;
    }
    state.xp += amount;
    state.totalCompleted = (state.totalCompleted || 0) + 1;
    var leveledUp = 0;
    while (state.xp >= state.xpNeeded && state.level < 1000) {
        state.xp -= state.xpNeeded;
        state.level++;
        state.xpNeeded = state.level * 50;
        leveledUp++;
    }
    if (leveledUp > 0) {
        showToast('Новый уровень! ' + state.level);
        checkAchievements();
        renderAchievements();
    }
    state.xpGivenToday = true;
    saveState();
}

// ============================================================
// ДОСТИЖЕНИЯ
// ============================================================
function checkAchievements() {
    var a = state.achievements || {};
    var updated = {};
    for (var key in a) { updated[key] = a[key]; }
    var changed = false;
    for (var i = 0; i < achievementsList.length; i++) {
        var ach = achievementsList[i];
        if (!updated[ach.id]) {
            var unlocked = checkAchievementCondition(ach.id);
            if (unlocked) {
                updated[ach.id] = true;
                changed = true;
                (function(name) {
                    setTimeout(function() {
                        showToast('Достижение: ' + name + '!');
                    }, 500);
                })(ach.name);
            }
        }
    }
    state.achievements = updated;
    if (changed) saveState();
}

function checkAchievementCondition(id) {
    switch(id) {
        case 'first': return state.habits.length >= 1;
        case 'week_streak': return state.streak >= 7;
        case 'month_streak': return state.streak >= 30;
        case 'year_streak': return state.streak >= 365;
        case 'hundred': return state.totalCompleted >= 100;
        case 'five_hundred': return state.totalCompleted >= 500;
        case 'thousand': return state.totalCompleted >= 1000;
        case 'level_5': return state.level >= 5;
        case 'level_10': return state.level >= 10;
        case 'level_25': return state.level >= 25;
        case 'level_50': return state.level >= 50;
        case 'level_100': return state.level >= 100;
        case 'habits_5': return state.habits.length >= 5;
        case 'habits_10': return state.habits.length >= 10;
        case 'habits_20': return state.habits.length >= 20;
        case 'streak_3': return state.streak >= 3;
        case 'streak_14': return state.streak >= 14;
        case 'streak_60': return state.streak >= 60;
        case 'streak_100': return state.streak >= 100;
        case 'points_100': return state.points >= 100;
        case 'points_500': return state.points >= 500;
        case 'points_1000': return state.points >= 1000;
        case 'streak_200': return state.streak >= 200;
        case 'streak_365': return state.streak >= 365;
        case 'habits_30': return state.habits.length >= 30;
        case 'habits_50': return state.habits.length >= 50;
        case 'level_200': return state.level >= 200;
        case 'level_500': return state.level >= 500;
        case 'level_1000': return state.level >= 1000;
        case 'premium_activate': return state.subscriptionType === 'premium';
        case 'veteran': return state.totalCompleted >= 5000;
        case 'morning': return false;
        case 'evening': return false;
        case 'perfect_day': return false;
        case 'perfect_week': return false;
        case 'perfect_month': return false;
        case 'friend_1': return false;
        case 'friend_5': return false;
        case 'friend_10': return false;
        case 'friend_25': return false;
        case 'friend_50': return false;
        case 'premium_year': return false;
        case 'morning_week': return false;
        case 'evening_week': return false;
        case 'perfect_year': return false;
        case 'no_skip_day': return false;
        case 'points_5000': return state.points >= 5000;
        case 'points_10000': return state.points >= 10000;
        case 'habits_all_types': return false;
        case 'super_veteran': return state.totalCompleted >= 10000;
        default: return false;
    }
}

function renderAchievements() {
    var list = document.getElementById('achievements-list');
    if (!list) return;
    var unlocked = state.achievements || {};
    var html = '';
    for (var i = 0; i < achievementsList.length; i++) {
        var ach = achievementsList[i];
        var isUnlocked = unlocked[ach.id] || false;
        html += '<div class="achievement-item ' + (isUnlocked ? 'unlocked' : '') + '">';
        html += '<div class="achievement-info" style="flex:1;">';
        html += '<div class="achievement-name">' + ach.name + '</div>';
        html += '<div class="achievement-desc">' + ach.desc + '</div>';
        html += '</div>';
        html += '<span class="achievement-status">' + (isUnlocked ? '✓' : '○') + '</span>';
        html += '</div>';
    }
    list.innerHTML = html;
}

// ============================================================
// ЛИДЕРБОРД
// ============================================================
function renderLeaderboard() {
    var list = document.getElementById('leaderboard-list');
    if (!list) return;
    var users = [
        { name: 'Алексей', score: 45 },
        { name: 'Мария', score: 42 },
        { name: 'Игорь', score: 38 },
        { name: 'Ты', score: state.totalCompleted || 10, isYou: true },
        { name: 'Ольга', score: 30 },
        { name: 'Сергей', score: 28 },
        { name: 'Анна', score: 25 },
        { name: 'Дмитрий', score: 20 }
    ];
    var html = '';
    for (var i = 0; i < users.length; i++) {
        var u = users[i];
        var cls = i === 0 ? 'gold' : i === 1 ? 'silver' : i === 2 ? 'bronze' : '';
        html += '<div class="rating-item" style="' + (u.isYou ? 'border:2px solid #ff6b8a;' : '') + '">';
        html += '<span class="rating-place ' + cls + '">' + (i+1) + '</span>';
        html += '<span class="rating-name">' + u.name + '</span>';
        html += '<span class="rating-score">' + u.score + '</span>';
        html += '</div>';
    }
    list.innerHTML = html;
}

// ============================================================
// СТАТИСТИКА
// ============================================================
function updateStats() {
    var today = new Date().toISOString().split('T')[0];
    var doneToday = 0;
    for (var i = 0; i < state.habits.length; i++) {
        var h = state.habits[i];
        if (h.logs) {
            for (var j = 0; j < h.logs.length; j++) {
                if (h.logs[j].date === today && h.logs[j].completed) {
                    doneToday++;
                    break;
                }
            }
        }
    }
    state.completedToday = doneToday;
    document.getElementById('today-count').textContent = doneToday;
    document.getElementById('streak-display').textContent = state.streak || 0;
    var fill = document.getElementById('xp-fill');
    if (fill) fill.style.width = Math.min(100, (state.xp / state.xpNeeded) * 100) + '%';
    document.getElementById('progress-level').textContent = state.level;
    document.getElementById('progress-xp').textContent = state.xp + ' / ' + state.xpNeeded + ' XP';
    document.getElementById('total-done').textContent = state.totalCompleted || 0;
    document.getElementById('max-streak').textContent = state.maxStreak || 0;
    renderCalendar();
    updateRemainingDays();
}

// ============================================================
// КАЛЕНДАРЬ
// ============================================================
function renderCalendar() {
    var grid = document.getElementById('calendar-grid');
    if (!grid) return;
    var today = new Date();
    var year = today.getFullYear();
    var month = today.getMonth();
    var daysInMonth = new Date(year, month + 1, 0).getDate();
    var firstDay = new Date(year, month, 1).getDay();
    var start = firstDay === 0 ? 6 : firstDay - 1;
    var html = '';
    var dayNames = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс'];
    for (var d = 0; d < dayNames.length; d++) {
        html += '<div class="cal-day cal-day-label">' + dayNames[d] + '</div>';
    }
    for (var i = 0; i < start; i++) {
        html += '<div class="cal-day empty"></div>';
    }
    for (var day = 1; day <= daysInMonth; day++) {
        var dateStr = year + '-' + String(month+1).padStart(2,'0') + '-' + String(day).padStart(2,'0');
        var completed = 0, total = 0;
        for (var h = 0; h < state.habits.length; h++) {
            var habit = state.habits[h];
            if (habit.logs) {
                for (var l = 0; l < habit.logs.length; l++) {
                    if (habit.logs[l].date === dateStr) {
                        total++;
                        if (habit.logs[l].completed) completed++;
                        break;
                    }
                }
            }
        }
        var status = '';
        if (total > 0 && completed === total) status = 'completed';
        else if (completed > 0) status = 'partial';
        var isToday = dateStr === today.toISOString().split('T')[0];
        html += '<div class="cal-day ' + status + (isToday ? ' today' : '') + '">' + day + '</div>';
    }
    grid.innerHTML = html;
}

// ============================================================
// НАВИГАЦИЯ
// ============================================================
function switchTab(tab) {
    state.currentTab = tab;
    var screens = document.querySelectorAll('.screen');
    for (var i = 0; i < screens.length; i++) {
        screens[i].classList.add('hidden');
    }
    var btns = document.querySelectorAll('.nav-btn');
    for (var j = 0; j < btns.length; j++) {
        btns[j].classList.toggle('active', btns[j].dataset.tab === tab);
        if (btns[j].dataset.tab === tab) {
            btns[j].classList.add('nav-active-bounce');
        } else {
            btns[j].classList.remove('nav-active-bounce');
        }
    }
    var el = document.getElementById(tab + '-screen');
    if (el) el.classList.remove('hidden');
    if (tab === 'progress') { updateStats(); renderCalendar(); }
    if (tab === 'rating') renderRating();
    if (tab === 'leaderboard') renderLeaderboard();
    if (tab === 'friends') renderFriends();
    if (tab === 'achievements') renderAchievements();
    if (tab === 'profile') renderProfile();
}

// ============================================================
// ОБРАБОТЧИКИ
// ============================================================
function setupEventListeners() {
    document.getElementById('theme-toggle').addEventListener('click', cycleTheme);

    document.getElementById('sub-trial-btn').addEventListener('click', function() {
        if (!state.trialUsed) {
            activateSubscription('trial');
        }
    });
    document.getElementById('sub-basic-btn').addEventListener('click', function() {
        activateSubscription('basic');
    });
    document.getElementById('sub-premium-btn').addEventListener('click', function() {
        activateSubscription('premium');
    });

    document.getElementById('welcome-start').addEventListener('click', function() {
        state.hasSeenWelcome = true;
        saveState();
        document.getElementById('welcome-screen').classList.add('hidden');
        if (!state.hasSeenOnboarding) {
            startOnboarding();
        } else {
            document.getElementById('main-interface').classList.remove('hidden');
            initApp();
        }
    });

    document.getElementById('onboarding-next').addEventListener('click', function() {
        if (onboardingStep < onboardingSteps.length - 1) {
            showOnboardingStep(onboardingStep + 1);
        } else {
            state.hasSeenOnboarding = true;
            saveState();
            document.getElementById('onboarding').classList.add('hidden');
            document.getElementById('main-interface').classList.remove('hidden');
            initApp();
        }
    });
    document.getElementById('onboarding-skip').addEventListener('click', function() {
        state.hasSeenOnboarding = true;
        saveState();
        document.getElementById('onboarding').classList.add('hidden');
        document.getElementById('main-interface').classList.remove('hidden');
        initApp();
    });

    document.getElementById('add-habit-btn').addEventListener('click', function() {
        document.getElementById('add-habit-modal').classList.remove('hidden');
        document.getElementById('habit-name-input').focus();
    });
    document.getElementById('close-modal-btn').addEventListener('click', function() {
        document.getElementById('add-habit-modal').classList.add('hidden');
    });
    document.getElementById('save-habit-btn').addEventListener('click', function() {
        var name = document.getElementById('habit-name-input').value.trim();
        if (name) {
            addHabit(name);
            document.getElementById('add-habit-modal').classList.add('hidden');
        } else showToast('Введите название');
    });
    document.getElementById('habit-name-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') document.getElementById('save-habit-btn').click();
    });

    var navBtns = document.querySelectorAll('.nav-btn');
    for (var i = 0; i < navBtns.length; i++) {
        (function(btn) {
            btn.addEventListener('click', function() {
                switchTab(btn.dataset.tab);
            });
        })(navBtns[i]);
    }

    var backBtns = document.querySelectorAll('.back-btn');
    for (var j = 0; j < backBtns.length; j++) {
        (function(btn) {
            btn.addEventListener('click', function() {
                switchTab('today');
            });
        })(backBtns[j]);
    }

    document.getElementById('subscription-btn').addEventListener('click', function() {
        showToast('Скоро здесь будет подписка');
    });
    document.getElementById('invite-btn').addEventListener('click', function() {
        showToast('Твоя ссылка скоро будет готова');
    });
    document.getElementById('add-habit-modal').addEventListener('click', function(e) {
        if (e.target === e.currentTarget) document.getElementById('add-habit-modal').classList.add('hidden');
    });

    document.getElementById('support-btn').addEventListener('click', function() {
        showSupportModal();
    });
}

function showSupportModal() {
    var overlay = document.createElement('div');
    overlay.className = 'modal support-modal-overlay';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'flex-end';
    overlay.style.justifyContent = 'center';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.background = 'rgba(0,0,0,0.3)';
    overlay.style.zIndex = '6000';

    var content = document.createElement('div');
    content.className = 'modal-content';
    content.style.background = 'var(--bg-card)';
    content.style.borderRadius = '20px 20px 0 0';
    content.style.padding = '24px 20px 32px';
    content.style.width = '100%';
    content.style.maxWidth = '420px';
    content.style.animation = 'slideUp 0.3s ease';

    content.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <h3 style="font-size:18px;font-weight:600;color:var(--text-primary);">Живая поддержка</h3>
            <button onclick="this.closest('.modal').remove()" style="background:none;border:none;font-size:24px;color:var(--text-secondary);cursor:pointer;">✕</button>
        </div>
        <p style="color:var(--text-secondary);margin-bottom:20px;font-size:15px;">Свяжись с нами удобным способом:</p>
        <div style="display:flex;flex-direction:column;gap:12px;">
            <a href="https://t.me/habitmon_support" target="_blank" style="display:flex;align-items:center;gap:12px;padding:14px 16px;border:2px solid var(--border-color);border-radius:12px;text-decoration:none;color:var(--text-primary);transition:all 0.2s;background:var(--bg-primary);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0088cc" stroke-width="2"><path d="M21 10.5h.375c.621 0 1.125.504 1.125 1.125v2.25c0 .621-.504 1.125-1.125 1.125H21M3.75 18h15A2.25 2.25 0 0 0 21 15.75v-6a2.25 2.25 0 0 0-2.25-2.25h-15A2.25 2.25 0 0 0 1.5 9.75v6A2.25 2.25 0 0 0 3.75 18Z"/></svg>
                <span>Telegram: @habitmon_support</span>
            </a>
            <a href="mailto:support@habitmon.com" target="_blank" style="display:flex;align-items:center;gap:12px;padding:14px 16px;border:2px solid var(--border-color);border-radius:12px;text-decoration:none;color:var(--text-primary);transition:all 0.2s;background:var(--bg-primary);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ea4335" stroke-width="2"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                <span>Email: support@habitmon.com</span>
            </a>
            <div style="display:flex;gap:12px;margin-top:8px;">
                <button onclick="showToast('Скоро ответим!')" style="flex:2;padding:14px;border:none;border-radius:12px;background:#ff6b8a;color:white;font-size:15px;font-weight:500;cursor:pointer;">Написать сейчас</button>
                <button onclick="this.closest('.modal').remove()" style="flex:1;padding:14px;border:none;border-radius:12px;background:var(--border-color);color:var(--text-primary);font-size:15px;cursor:pointer;">Закрыть</button>
            </div>
        </div>
    `;

    overlay.appendChild(content);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) overlay.remove();
    });
}

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ
// ============================================================
function renderRating() {
    var list = document.getElementById('rating-list');
    var users = [
        { name: 'Алексей', score: 45 },
        { name: 'Мария', score: 42 },
        { name: 'Игорь', score: 38 },
        { name: 'Ты', score: state.totalCompleted || 10, isYou: true },
        { name: 'Ольга', score: 30 }
    ];
    var html = '';
    for (var i = 0; i < users.length; i++) {
        var u = users[i];
        var cls = i === 0 ? 'gold' : i === 1 ? 'silver' : i === 2 ? 'bronze' : '';
        html += '<div class="rating-item" style="' + (u.isYou ? 'border:2px solid #ff6b8a;' : '') + '">';
        html += '<span class="rating-place ' + cls + '">' + (i+1) + '</span>';
        html += '<span class="rating-name">' + u.name + '</span>';
        html += '<span class="rating-score">' + u.score + '</span>';
        html += '</div>';
    }
    list.innerHTML = html;
}

function renderFriends() {
    document.getElementById('friends-list').innerHTML = '<p class="empty-habits">Пригласи друзей и соревнуйся с ними</p>';
}

function renderProfile() {
    document.getElementById('profile-name').textContent = state.username || 'Пользователь';
    document.getElementById('profile-level').textContent = state.level;
    document.getElementById('profile-points').textContent = state.points;
    document.getElementById('profile-streak').textContent = state.streak || 0;
    document.getElementById('profile-total').textContent = state.totalCompleted || 0;
    updateRemainingDays();
}

function showToast(msg) {
    var existing = document.querySelectorAll('.toast');
    for (var i = 0; i < existing.length; i++) {
        existing[i].remove();
    }
    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(function() {
        if (toast.parentNode) toast.remove();
    }, 3000);
}
