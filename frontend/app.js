/**
 * EcoHarvest Farm - Appointment Booking System
 * Vue.js 3 Frontend Application
 * 
 * A modern, responsive Vue application for booking appointments
 * with real-time notifications and calendar management.
 */

const { createApp, ref, reactive, computed, onMounted, onUnmounted } = Vue;

// ============================================================================
// CONFIGURATION
// ============================================================================

// Use environment variables for deployment, fallback to localhost for development
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api'
    : (window.API_BASE_URL || 'https://your-railway-app.railway.app/api');

const WS_URL = window.location.hostname === 'localhost'
    ? 'ws://localhost:8000/ws/notifications'
    : (window.WS_URL || 'wss://your-railway-app.railway.app/ws/notifications');

// ============================================================================
// VUE APP DEFINITION
// ============================================================================

const app = createApp({
    template: `
        <div class="min-h-screen py-8 px-4">
            <div class="max-w-6xl mx-auto">
                <!-- Header with Farm Branding -->
                <div class="header-farm rounded-xl p-6 mb-8 shadow-2xl">
                    <div class="flex justify-between items-center flex-wrap gap-4">
                        <div class="flex items-center gap-4">
                            <div class="farm-icon text-4xl">🌾</div>
                            <div>
                                <h1 class="text-4xl font-bold text-white mb-2">
                                    EcoHarvest Farm
                                </h1>
                                <p class="text-green-100 flex items-center gap-2">
                                    <span>🌱</span>
                                    Sustainable Farming Consultation Services
                                    <span>🌱</span>
                                </p>
                            </div>
                        </div>
                        <div v-if="isAdmin" class="notification-center">
                            <div class="relative">
                                <button @click="showNotifications = !showNotifications" class="text-3xl hover:scale-110 transition">
                                    🔔
                                    <span v-if="unreadCount > 0" class="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                                        {{ unreadCount }}
                                    </span>
                                </button>
                                <div v-if="showNotifications" class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-2xl z-50 max-h-96 overflow-y-auto">
                                    <div class="p-4 border-b font-bold text-gray-900">🔔 Notifications</div>
                                    <div v-if="notifications.length === 0" class="p-4 text-gray-500 text-center">
                                        No notifications yet
                                    </div>
                                    <div v-for="notif in notifications" :key="notif.id" class="p-4 border-b hover:bg-gray-50">
                                        <p class="font-semibold text-gray-900">🌾 {{ notif.title }}</p>
                                        <p class="text-sm text-gray-600">{{ notif.message }}</p>
                                        <p class="text-xs text-gray-400 mt-1">{{ formatTime(notif.created_at) }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="farm-divider"></div>
                    <p class="text-green-100 text-sm mt-4">
                        📍 Schedule your consultation with our farming experts | 🌍 Eco-friendly practices | 🚜 Expert guidance
                    </p>
                </div>

                <!-- Navigation Tabs -->
                <div class="flex gap-4 mb-8 flex-wrap">
                    <button
                        v-if="!isLoggedIn && !isAdmin"
                        @click="activeTab = 'login'"
                        :class="['px-6 py-3 rounded-lg font-semibold smooth-transition flex items-center gap-2', 
                                 activeTab === 'login' 
                                    ? 'glass-effect text-green-700 shadow-lg border-2 border-green-500' 
                                    : 'text-white hover:text-opacity-80 hover:bg-white hover:bg-opacity-10']"
                    >
                        <span>👤</span> Login / Register
                    </button>
                    <button
                        v-if="isLoggedIn"
                        @click="activeTab = 'dashboard'"
                        :class="['px-6 py-3 rounded-lg font-semibold smooth-transition flex items-center gap-2', 
                                 activeTab === 'dashboard' 
                                    ? 'glass-effect text-green-700 shadow-lg border-2 border-green-500' 
                                    : 'text-white hover:text-opacity-80 hover:bg-white hover:bg-opacity-10']"
                    >
                        <span>📊</span> My Dashboard
                    </button>
                    <button
                        v-if="!isAdmin"
                        @click="activeTab = 'booking'"
                        :class="['px-6 py-3 rounded-lg font-semibold smooth-transition flex items-center gap-2', 
                                 activeTab === 'booking' 
                                    ? 'glass-effect text-green-700 shadow-lg border-2 border-green-500' 
                                    : 'text-white hover:text-opacity-80 hover:bg-white hover:bg-opacity-10']"
                    >
                        <span>📅</span> Book Consultation
                    </button>
                    <button
                        v-if="isAdmin"
                        @click="activeTab = 'calendar'"
                        :class="['px-6 py-3 rounded-lg font-semibold smooth-transition flex items-center gap-2',
                                 activeTab === 'calendar'
                                    ? 'glass-effect text-green-700 shadow-lg border-2 border-green-500'
                                    : 'text-white hover:text-opacity-80 hover:bg-white hover:bg-opacity-10']"
                    >
                        <span>🗓️</span> View Schedule
                    </button>
                    <button
                        v-if="isAdmin"
                        @click="logoutAdmin"
                        class="px-6 py-3 rounded-lg font-semibold smooth-transition flex items-center gap-2 text-white hover:text-opacity-80 hover:bg-white hover:bg-opacity-10"
                    >
                        <span>🚪</span> Logout
                    </button>
                    <button
                        v-if="isLoggedIn"
                        @click="logoutClient"
                        class="px-6 py-3 rounded-lg font-semibold smooth-transition flex items-center gap-2 text-white hover:text-opacity-80 hover:bg-white hover:bg-opacity-10"
                    >
                        <span>🚪</span> Logout
                    </button>
                </div>

                <!-- Admin Login Modal -->
                <div v-if="showAdminLogin && !isAdmin" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg p-8 shadow-2xl max-w-md w-full mx-4">
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">🔐 Admin Login</h3>
                        <input
                            :value="adminPassword"
                            @input="adminPassword = $event.target.value"
                            type="password"
                            placeholder="Enter admin password"
                            @keyup.enter="checkAdminPassword"
                            class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 mb-4"
                        />
                        <div class="flex gap-2">
                            <button
                                @click="checkAdminPassword"
                                class="flex-1 py-2 px-4 bg-green-500 text-white font-bold rounded-lg hover:bg-green-600"
                            >
                                Login
                            </button>
                            <button
                                @click="showAdminLogin = false; adminPassword = ''"
                                class="flex-1 py-2 px-4 bg-gray-300 text-gray-800 font-bold rounded-lg hover:bg-gray-400"
                            >
                                Cancel
                            </button>
                        </div>
                        <p v-if="adminError" class="text-red-600 text-sm mt-2">{{ adminError }}</p>
                    </div>
                </div>

                <!-- Login/Register Tab -->
                <div v-if="activeTab === 'login'" class="glass-effect rounded-xl p-8 shadow-2xl farm-card">
                    <div class="flex items-center gap-3 mb-6">
                        <span class="text-3xl farm-icon">👤</span>
                        <h2 class="text-3xl font-bold gradient-text">{{ showRegister ? 'Create Account' : 'Login' }}</h2>
                    </div>

                    <div v-if="authError" class="mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg text-red-700 flex items-start gap-3">
                        <span class="text-xl">⚠️</span>
                        <div>{{ authError }}</div>
                    </div>

                    <div v-if="authSuccess" class="mb-4 p-4 bg-green-50 border-l-4 border-green-500 rounded-lg text-green-700 flex items-start gap-3">
                        <span class="text-xl">✅</span>
                        <div>{{ authSuccess }}</div>
                    </div>

                    <form @submit.prevent="handleAuth" class="space-y-4 max-w-md">
                        <div v-if="showRegister">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name *</label>
                            <input
                                v-model="authForm.name"
                                type="text"
                                required
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                placeholder="John Doe"
                            />
                        </div>

                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Email *</label>
                            <input
                                v-model="authForm.email"
                                type="email"
                                required
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                placeholder="john@example.com"
                            />
                        </div>

                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Password *</label>
                            <input
                                v-model="authForm.password"
                                type="password"
                                required
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                placeholder="••••••••"
                            />
                        </div>

                        <div v-if="showRegister">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Confirm Password *</label>
                            <input
                                v-model="authForm.confirmPassword"
                                type="password"
                                required
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                placeholder="••••••••"
                            />
                        </div>

                        <button
                            type="submit"
                            :disabled="authLoading"
                            class="w-full py-3 px-4 harvest-button font-bold rounded-lg hover:shadow-lg smooth-transition disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                            <span v-if="authLoading" class="animate-spin">⏳</span>
                            <span v-if="!authLoading">🌾</span>
                            {{ authLoading ? (showRegister ? 'Creating Account...' : 'Logging In...') : (showRegister ? 'Create Account' : 'Login') }}
                        </button>

                        <button
                            type="button"
                            @click="showRegister = !showRegister"
                            class="w-full py-2 px-4 text-green-600 font-semibold hover:text-green-800"
                        >
                            {{ showRegister ? 'Already have an account? Login' : "Don't have an account? Register" }}
                        </button>

                        <button
                            v-if="!showRegister"
                            type="button"
                            @click="showForgotPassword = true"
                            class="w-full py-2 px-4 text-sm text-gray-600 font-semibold hover:text-gray-800"
                        >
                            Forgot Password?
                        </button>
                    </form>
                </div>

                <!-- Client Dashboard Tab -->
                <div v-if="activeTab === 'dashboard'" class="glass-effect rounded-xl p-8 shadow-2xl farm-card">
                    <div class="flex items-center gap-3 mb-6">
                        <span class="text-3xl farm-icon">📊</span>
                        <h2 class="text-3xl font-bold gradient-text">My Dashboard</h2>
                    </div>
                    <p class="text-gray-600 mb-6 flex items-center gap-2">
                        <span>👤</span> Welcome, {{ currentUser?.name || 'Client' }}!
                    </p>

                    <!-- Current/Upcoming Appointments -->
                    <div class="mb-8">
                        <h3 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                            <span>📅</span> Upcoming Appointments
                        </h3>
                        <div v-if="upcomingAppointments.length === 0" class="text-center py-8 text-gray-500">
                            <p class="text-2xl mb-2">🌱</p>
                            <p>No upcoming appointments. Book one now!</p>
                        </div>
                        <div v-else class="space-y-3">
                            <div v-for="apt in upcomingAppointments" :key="apt.id" class="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                                <div class="flex justify-between items-start">
                                    <div>
                                        <p class="font-bold text-gray-900 flex items-center gap-2">
                                            <span>📅</span> {{ formatDate(apt.appointment_time) }}
                                        </p>
                                        <p class="text-sm text-gray-600 flex items-center gap-2 mt-1">
                                            <span>⏰</span> {{ formatTime(apt.appointment_time) }}
                                        </p>
                                        <p v-if="apt.notes" class="text-sm text-gray-600 mt-2">📝 {{ apt.notes }}</p>
                                    </div>
                                    <span :class="['px-3 py-1 text-xs font-semibold rounded-full',
                                                   apt.status === 'confirmed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800']">
                                        {{ apt.status === 'confirmed' ? '✅ Confirmed' : '⏳ Pending' }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Appointment History -->
                    <div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                            <span>📜</span> Appointment History
                        </h3>
                        <div v-if="appointmentHistory.length === 0" class="text-center py-8 text-gray-500">
                            <p>No past appointments yet.</p>
                        </div>
                        <div v-else class="space-y-3 max-h-64 overflow-y-auto">
                            <div v-for="apt in appointmentHistory" :key="apt.id" class="p-4 bg-gray-50 rounded-lg border-l-4 border-gray-400">
                                <div class="flex justify-between items-start">
                                    <div>
                                        <p class="font-bold text-gray-900 flex items-center gap-2">
                                            <span>📅</span> {{ formatDate(apt.appointment_time) }}
                                        </p>
                                        <p class="text-sm text-gray-600 flex items-center gap-2 mt-1">
                                            <span>⏰</span> {{ formatTime(apt.appointment_time) }}
                                        </p>
                                    </div>
                                    <span :class="['px-3 py-1 text-xs font-semibold rounded-full',
                                                   apt.status === 'confirmed' ? 'bg-green-100 text-green-800' : apt.status === 'cancelled' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800']">
                                        {{ apt.status }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Booking Form Tab -->
                <div v-if="activeTab === 'booking' && !isAdmin" class="glass-effect rounded-xl p-8 shadow-2xl farm-card">
                    <div class="flex items-center gap-3 mb-6">
                        <span class="text-3xl farm-icon">🌾</span>
                        <h2 class="text-3xl font-bold gradient-text">Book Your Consultation</h2>
                    </div>
                    <p class="text-gray-600 mb-6 flex items-center gap-2">
                        <span>🌱</span> Schedule a consultation with our farming experts
                    </p>

                    <div v-if="formError" class="mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg text-red-700 flex items-start gap-3">
                        <span class="text-xl">⚠️</span>
                        <div>{{ formError }}</div>
                    </div>

                    <div v-if="formSuccess" class="mb-4 p-4 bg-green-50 border-l-4 border-green-500 rounded-lg text-green-700 flex items-start gap-3">
                        <span class="text-xl">✅</span>
                        <div>{{ formSuccess }}</div>
                    </div>

                    <form @submit.prevent="submitBooking" class="space-y-4">
                        <!-- Name Field - Hidden if logged in -->
                        <div v-if="!isLoggedIn">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">
                                👤 Full Name *
                            </label>
                            <input
                                v-model="bookingForm.client_name"
                                type="text"
                                required
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 smooth-transition"
                                placeholder="John Doe"
                            />
                        </div>
                        <div v-else class="p-3 bg-green-50 border-l-4 border-green-500 rounded-lg text-green-700">
                            <span class="font-semibold">👤 Name:</span> {{ currentUser.name }}
                        </div>

                        <!-- Email Field - Hidden if logged in -->
                        <div v-if="!isLoggedIn">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">
                                📧 Email Address *
                            </label>
                            <input
                                v-model="bookingForm.client_email"
                                type="email"
                                required
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 smooth-transition"
                                placeholder="john@example.com"
                            />
                        </div>
                        <div v-else class="p-3 bg-green-50 border-l-4 border-green-500 rounded-lg text-green-700">
                            <span class="font-semibold">📧 Email:</span> {{ currentUser.email }}
                        </div>

                        <!-- Phone Field -->
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">
                                📱 Phone Number
                            </label>
                            <input
                                v-model="bookingForm.client_phone"
                                type="tel"
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 smooth-transition"
                                placeholder="+1234567890"
                            />
                        </div>

                        <!-- Date Field -->
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">
                                📅 Preferred Date *
                            </label>
                            <input
                                v-model="selectedDate"
                                type="date"
                                :min="minDate"
                                required
                                @change="loadAvailableSlots"
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 smooth-transition"
                            />
                        </div>

                        <!-- Time Slot Selection -->
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">
                                ⏰ Preferred Time *
                            </label>
                            <div v-if="!selectedDate" class="text-center py-4 text-gray-500">
                                Please select a date first
                            </div>
                            <div v-else-if="loadingSlots" class="text-center py-4 text-gray-500">
                                Loading available slots...
                            </div>
                            <div v-else-if="availableSlots.length === 0" class="text-center py-4 text-gray-500">
                                No available slots for this date
                            </div>
                            <div v-else class="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto">
                                <button
                                    v-for="slot in availableSlots"
                                    :key="slot.time"
                                    type="button"
                                    @click="bookingForm.appointment_time = slot.time"
                                    :class="['px-4 py-2 rounded-lg font-semibold transition',
                                             slot.is_available
                                                ? bookingForm.appointment_time === slot.time
                                                    ? 'bg-green-500 text-white'
                                                    : 'bg-green-100 text-green-800 hover:bg-green-200'
                                                : 'bg-gray-200 text-gray-400 cursor-not-allowed']"
                                    :disabled="!slot.is_available"
                                >
                                    {{ slot.is_available ? '🟢' : '🔴' }} {{ formatSlotTime(slot.time) }}
                                </button>
                            </div>
                        </div>

                        <!-- Notes Field -->
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">
                                📝 Additional Notes
                            </label>
                            <textarea
                                v-model="bookingForm.notes"
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 smooth-transition"
                                placeholder="Any special requests or farming topics you'd like to discuss..."
                                rows="3"
                            ></textarea>
                        </div>

                        <!-- Terms and Conditions -->
                        <div class="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                            <h3 class="font-bold text-gray-900 mb-3 flex items-center gap-2">
                                <span>📋</span> Terms & Conditions
                            </h3>
                            <button
                                type="button"
                                @click="showTermsModal = true"
                                class="text-blue-600 hover:text-blue-800 underline mb-3 text-sm font-semibold"
                            >
                                📖 Click here to read full terms and conditions
                            </button>
                            <label class="flex items-center gap-3 cursor-pointer">
                                <input
                                    v-model="bookingForm.agreedToTerms"
                                    type="checkbox"
                                    class="w-5 h-5 accent-green-600 cursor-pointer"
                                />
                                <span class="font-semibold text-gray-900">I agree to the terms and conditions *</span>
                            </label>
                        </div>

                        <!-- Submit Button -->
                        <button
                            type="submit"
                            :disabled="bookingLoading || !bookingForm.agreedToTerms"
                            class="w-full py-3 px-4 harvest-button font-bold rounded-lg hover:shadow-lg smooth-transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            <span v-if="bookingLoading" class="animate-spin">⏳</span>
                            <span v-if="!bookingLoading">🌾</span>
                            {{ bookingLoading ? 'Booking Consultation...' : 'Book Consultation' }}
                        </button>
                    </form>
                </div>

                <!-- Calendar View Tab -->
                <div v-if="activeTab === 'calendar'" class="glass-effect rounded-xl p-8 shadow-2xl farm-card">
                    <div class="flex items-center gap-3 mb-6">
                        <span class="text-3xl farm-icon">🗓️</span>
                        <h2 class="text-3xl font-bold gradient-text">Consultation Management</h2>
                    </div>

                    <!-- Admin Calendar Tabs -->
                    <div class="flex gap-2 mb-6 flex-wrap">
                        <button
                            @click="adminCalendarView = 'upcoming'"
                            :class="['px-4 py-2 rounded-lg font-semibold smooth-transition', 
                                     adminCalendarView === 'upcoming' 
                                        ? 'bg-green-500 text-white shadow-lg' 
                                        : 'bg-gray-200 text-gray-800 hover:bg-gray-300']"
                        >
                            📅 Upcoming
                        </button>
                        <button
                            @click="adminCalendarView = 'monthly'"
                            :class="['px-4 py-2 rounded-lg font-semibold smooth-transition', 
                                     adminCalendarView === 'monthly' 
                                        ? 'bg-green-500 text-white shadow-lg' 
                                        : 'bg-gray-200 text-gray-800 hover:bg-gray-300']"
                        >
                            📆 Monthly
                        </button>
                        <button
                            @click="adminCalendarView = 'weekly'"
                            :class="['px-4 py-2 rounded-lg font-semibold smooth-transition', 
                                     adminCalendarView === 'weekly' 
                                        ? 'bg-green-500 text-white shadow-lg' 
                                        : 'bg-gray-200 text-gray-800 hover:bg-gray-300']"
                        >
                            📋 Weekly
                        </button>
                        <button
                            @click="adminCalendarView = 'past'"
                            :class="['px-4 py-2 rounded-lg font-semibold smooth-transition', 
                                     adminCalendarView === 'past' 
                                        ? 'bg-blue-500 text-white shadow-lg' 
                                        : 'bg-gray-200 text-gray-800 hover:bg-gray-300']"
                        >
                            ✅ Past
                        </button>
                        <button
                            @click="adminCalendarView = 'cancelled'"
                            :class="['px-4 py-2 rounded-lg font-semibold smooth-transition', 
                                     adminCalendarView === 'cancelled' 
                                        ? 'bg-red-500 text-white shadow-lg' 
                                        : 'bg-gray-200 text-gray-800 hover:bg-gray-300']"
                        >
                            ❌ Cancelled
                        </button>
                    </div>

                    <!-- Upcoming/Monthly/Weekly View -->
                    <div v-if="['upcoming', 'monthly', 'weekly'].includes(adminCalendarView)">
                        <div v-if="loadingCalendar" class="text-center py-8 text-gray-500 flex items-center justify-center gap-2">
                            <span class="animate-spin">🌾</span> Loading schedule...
                        </div>
                        <div v-else-if="Object.keys(calendar).length === 0" class="text-center py-8 text-gray-500">
                            <p class="text-2xl mb-2">🌱</p>
                            <p>No consultations scheduled yet.</p>
                        </div>
                        <div v-else class="space-y-4">
                            <div v-for="(appointments, date) in sortedCalendar" :key="date" class="border-l-4 border-green-500 bg-gradient-to-r from-green-50 to-transparent rounded-lg p-4 hover:shadow-md smooth-transition">
                                <h3 class="font-bold text-lg text-green-900 mb-3 flex items-center gap-2">
                                    <span>📅</span>
                                    {{ formatDate(date) }}
                                </h3>
                                <div class="space-y-2">
                                    <div v-for="apt in appointments" :key="apt.id" class="p-4 bg-white rounded-lg border-l-4 border-green-400 hover:shadow-md smooth-transition">
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                            <div>
                                                <p class="font-semibold text-gray-900 flex items-center gap-2 mb-2">
                                                    <span>👤</span> {{ apt.client_name }}
                                                </p>
                                                <p class="text-sm text-gray-600 flex items-center gap-2 mb-1">
                                                    <span>📧</span> {{ apt.client_email }}
                                                </p>
                                                <p class="text-sm text-gray-600 flex items-center gap-2">
                                                    <span>📱</span> {{ apt.client_phone || 'N/A' }}
                                                </p>
                                            </div>
                                            <div class="text-right">
                                                <p class="font-semibold text-green-700 flex items-center justify-end gap-2 mb-2">
                                                    <span>⏰</span>
                                                    {{ formatTime(apt.start_time) }}
                                                </p>
                                                <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800 flex items-center gap-1 justify-end">
                                                    ✅ {{ apt.status }}
                                                </span>
                                            </div>
                                        </div>
                                        <div v-if="apt.notes" class="mb-3 p-2 bg-blue-50 rounded border-l-2 border-blue-400">
                                            <p class="text-xs font-semibold text-blue-900 mb-1">📝 Notes:</p>
                                            <p class="text-sm text-blue-800">{{ apt.notes }}</p>
                                        </div>
                                        <div class="flex gap-2">
                                            <button
                                                @click="openCancelModal(apt)"
                                                class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 font-semibold flex items-center gap-2"
                                            >
                                                <span>❌</span> Cancel
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Past Appointments -->
                    <div v-if="adminCalendarView === 'past'" class="space-y-4">
                        <div v-if="pastAppointments.length === 0" class="text-center py-8 text-gray-500">
                            <p class="text-2xl mb-2">📭</p>
                            <p>No past appointments yet.</p>
                        </div>
                        <div v-else>
                            <div v-for="apt in pastAppointments" :key="apt.id" class="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400 hover:shadow-md smooth-transition">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                    <div>
                                        <p class="font-semibold text-gray-900 flex items-center gap-2 mb-2">
                                            <span>👤</span> {{ apt.client_name }}
                                        </p>
                                        <p class="text-sm text-gray-600 flex items-center gap-2 mb-1">
                                            <span>📧</span> {{ apt.client_email }}
                                        </p>
                                        <p class="text-sm text-gray-600 flex items-center gap-2">
                                            <span>📱</span> {{ apt.client_phone || 'N/A' }}
                                        </p>
                                    </div>
                                    <div class="text-right">
                                        <p class="font-semibold text-blue-700 flex items-center justify-end gap-2 mb-2">
                                            <span>⏰</span>
                                            {{ formatTime(apt.start_time) }}
                                        </p>
                                        <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                                            ✅ Completed
                                        </span>
                                    </div>
                                </div>
                                <div v-if="apt.notes" class="p-2 bg-white rounded border-l-2 border-blue-400">
                                    <p class="text-xs font-semibold text-gray-900 mb-1">📝 Notes:</p>
                                    <p class="text-sm text-gray-700">{{ apt.notes }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Cancelled Appointments -->
                    <div v-if="adminCalendarView === 'cancelled'" class="space-y-4">
                        <div v-if="cancelledAppointments.length === 0" class="text-center py-8 text-gray-500">
                            <p class="text-2xl mb-2">📭</p>
                            <p>No cancelled appointments.</p>
                        </div>
                        <div v-else>
                            <div v-for="apt in cancelledAppointments" :key="apt.id" class="p-4 bg-red-50 rounded-lg border-l-4 border-red-400 hover:shadow-md smooth-transition">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                    <div>
                                        <p class="font-semibold text-gray-900 flex items-center gap-2 mb-2">
                                            <span>👤</span> {{ apt.client_name }}
                                        </p>
                                        <p class="text-sm text-gray-600 flex items-center gap-2 mb-1">
                                            <span>📧</span> {{ apt.client_email }}
                                        </p>
                                        <p class="text-sm text-gray-600 flex items-center gap-2">
                                            <span>📱</span> {{ apt.client_phone || 'N/A' }}
                                        </p>
                                    </div>
                                    <div class="text-right">
                                        <p class="font-semibold text-red-700 flex items-center justify-end gap-2 mb-2">
                                            <span>⏰</span>
                                            {{ formatTime(apt.start_time) }}
                                        </p>
                                        <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800">
                                            ❌ Cancelled
                                        </span>
                                    </div>
                                </div>
                                <div v-if="apt.notes" class="p-2 bg-white rounded border-l-2 border-red-400">
                                    <p class="text-xs font-semibold text-gray-900 mb-1">📝 Notes:</p>
                                    <p class="text-sm text-gray-700">{{ apt.notes }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Terms and Conditions Modal -->
                <div v-if="showTermsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg p-8 shadow-2xl max-w-2xl w-full mx-4 max-h-96 overflow-y-auto">
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">📋 Terms & Conditions</h3>
                        <div class="space-y-4 text-gray-700">
                            <div>
                                <p class="font-bold text-lg mb-2">1. Company Rights</p>
                                <p>The company has the right to reschedule or entirely cancel an appointment if necessary.</p>
                            </div>
                            <div>
                                <p class="font-bold text-lg mb-2">2. Client Cancellation Policy</p>
                                <p>If you as the client cancel the appointment, 20% of the consultation fees is retained by the company.</p>
                            </div>
                            <div>
                                <p class="font-bold text-lg mb-2">3. Company Cancellation Refund</p>
                                <p>If the company cancels an appointment, you are guaranteed a full refund.</p>
                            </div>
                            <div>
                                <p class="font-bold text-lg mb-2">4. Call Consultation Option</p>
                                <p>The company might decide to do a call consultation if needed (at a reduced price of course).</p>
                            </div>
                        </div>
                        <button
                            @click="showTermsModal = false"
                            class="mt-6 w-full py-2 px-4 bg-green-500 text-white font-bold rounded-lg hover:bg-green-600"
                        >
                            Close
                        </button>
                    </div>
                </div>

                <!-- Cancel Appointment Modal -->
                <div v-if="showCancelModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg p-8 shadow-2xl max-w-md w-full mx-4">
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">❌ Cancel Appointment</h3>
                        <p class="text-gray-600 mb-4">
                            Are you sure you want to cancel the appointment for <strong>{{ selectedAppointment?.client_name }}</strong> on {{ formatDate(selectedAppointment?.appointment_time) }}?
                        </p>
                        <div class="mb-4">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">
                                📧 Cancellation Message (will be sent to client):
                            </label>
                            <textarea
                                v-model="cancellationMessage"
                                placeholder="Enter reason for cancellation..."
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
                                rows="4"
                            ></textarea>
                        </div>
                        <div class="flex gap-2">
                            <button
                                @click="cancelAppointment"
                                class="flex-1 py-2 px-4 bg-red-500 text-white font-bold rounded-lg hover:bg-red-600"
                            >
                                Confirm Cancel
                            </button>
                            <button
                                @click="showCancelModal = false; cancellationMessage = ''"
                                class="flex-1 py-2 px-4 bg-gray-300 text-gray-800 font-bold rounded-lg hover:bg-gray-400"
                            >
                                Keep It
                            </button>
                        </div>
                        <p v-if="cancelError" class="text-red-600 text-sm mt-2">{{ cancelError }}</p>
                        <p v-if="cancelSuccess" class="text-green-600 text-sm mt-2">{{ cancelSuccess }}</p>
                    </div>
                </div>

                <!-- Forgot Password Modal -->
                <div v-if="showForgotPassword" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg p-8 shadow-2xl max-w-md w-full mx-4">
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">🔐 Reset Password</h3>
                        
                        <div v-if="forgotPasswordStep === 1">
                            <p class="text-gray-600 mb-4">Enter your email address to receive a password reset link.</p>
                            <input
                                v-model="forgotPasswordEmail"
                                type="email"
                                placeholder="your@email.com"
                                class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 mb-4"
                            />
                            <div v-if="forgotPasswordError" class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm rounded">
                                {{ forgotPasswordError }}
                            </div>
                            <div class="flex gap-2">
                                <button
                                    @click="sendPasswordResetEmail"
                                    :disabled="!forgotPasswordEmail || forgotPasswordLoading"
                                    class="flex-1 py-2 px-4 bg-green-500 text-white font-bold rounded-lg hover:bg-green-600 disabled:opacity-50"
                                >
                                    {{ forgotPasswordLoading ? 'Sending...' : 'Send Reset Link' }}
                                </button>
                                <button
                                    @click="showForgotPassword = false; forgotPasswordEmail = ''; forgotPasswordError = ''; forgotPasswordStep = 1"
                                    class="flex-1 py-2 px-4 bg-gray-300 text-gray-800 font-bold rounded-lg hover:bg-gray-400"
                                >
                                    Cancel
                                </button>
                            </div>
                        </div>

                        <div v-if="forgotPasswordStep === 2" class="text-center">
                            <p class="text-2xl mb-3">✅</p>
                            <p class="text-gray-700 font-semibold mb-4">Check your email!</p>
                            <p class="text-gray-600 mb-4">We've sent a password reset link to <strong>{{ forgotPasswordEmail }}</strong></p>
                            <p class="text-sm text-gray-500 mb-4">The link will expire in 24 hours.</p>
                            <button
                                @click="showForgotPassword = false; forgotPasswordEmail = ''; forgotPasswordStep = 1"
                                class="w-full py-2 px-4 bg-green-500 text-white font-bold rounded-lg hover:bg-green-600"
                            >
                                Done
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="mt-12 text-center text-white text-opacity-80 text-sm">
                    <div class="farm-divider"></div>
                    <div class="flex justify-center gap-4 mb-4">
                        <span class="text-2xl">🌾</span>
                        <span class="text-2xl">🌱</span>
                        <span class="text-2xl">🚜</span>
                        <span class="text-2xl">🌍</span>
                        <span class="text-2xl">♻️</span>
                    </div>
                    <p class="font-semibold">© 2024 EcoHarvest Farm - Sustainable Agriculture Consulting</p>
                    <p class="mt-2">📞 Expert Consultation Hours: 8:00 AM - 6:00 PM | ⏱️ Session Duration: 1 Hour</p>
                    <p class="mt-2 text-green-200">🌿 Committed to sustainable and eco-friendly farming practices</p>
                </div>
            </div>
        </div>
    `,
    setup() {
        // Check if admin route is accessed
        const urlParams = new URLSearchParams(window.location.search);
        const adminRoute = urlParams.get('admin');
        
        const activeTab = ref('booking');
        const showNotifications = ref(false);
        const bookingLoading = ref(false);
        const loadingSlots = ref(false);
        const loadingCalendar = ref(false);
        const formError = ref('');
        const formSuccess = ref('');
        const selectedDate = ref('');
        const minDate = ref('');
        const availableSlots = ref([]);
        const calendar = ref({});
        const notifications = ref([]);
        const unreadCount = ref(0);
        const isAdmin = ref(false);
        const showAdminLogin = ref(false);
        const adminPassword = ref('');
        const adminError = ref('');
        const ADMIN_PASSWORD = 'ecoharvest2024';
        const showCancelModal = ref(false);
        const selectedAppointment = ref(null);
        const cancellationMessage = ref('');
        const cancelError = ref('');
        const cancelSuccess = ref('');
        const showTermsModal = ref(false);
        const isLoggedIn = ref(false);
        const currentUser = ref(null);
        const showRegister = ref(false);
        const authLoading = ref(false);
        const adminCalendarView = ref('upcoming');
        const pastAppointments = ref([]);
        const cancelledAppointments = ref([]);
        const authError = ref('');
        const authSuccess = ref('');
        const upcomingAppointments = ref([]);
        const appointmentHistory = ref([]);
        const showForgotPassword = ref(false);
        const forgotPasswordEmail = ref('');
        const forgotPasswordError = ref('');
        const forgotPasswordLoading = ref(false);
        const forgotPasswordStep = ref(1);
        let ws = null;

        const bookingForm = reactive({
            client_name: '',
            client_email: '',
            client_phone: '',
            appointment_time: '',
            notes: '',
            agreedToTerms: false
        });

        const authForm = reactive({
            name: '',
            email: '',
            password: '',
            confirmPassword: ''
        });

        const sortedCalendar = computed(() => {
            const sorted = {};
            Object.keys(calendar.value).sort().forEach(date => {
                sorted[date] = calendar.value[date];
            });
            return sorted;
        });

        const formatDate = (dateStr) => {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        };

        const formatTime = (timeStr) => {
            if (!timeStr) return '';
            if (typeof timeStr === 'string' && timeStr.includes('T')) {
                const date = new Date(timeStr);
                return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            }
            return timeStr;
        };

        const formatSlotTime = (timeStr) => {
            if (!timeStr) return '';
            if (typeof timeStr === 'string' && timeStr.includes('T')) {
                const date = new Date(timeStr);
                return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
            }
            return timeStr;
        };

        const getMinDate = () => {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            return tomorrow.toISOString().split('T')[0];
        };

        const loadAvailableSlots = async () => {
            if (!selectedDate.value) return;
            loadingSlots.value = true;
            try {
                const url = `${API_BASE_URL}/available-slots?date=${selectedDate.value}`;
                console.log('Fetching slots from:', url);
                const response = await fetch(url);
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('API Error:', response.status, errorText);
                    throw new Error(`Failed to fetch slots: ${response.status}`);
                }
                const data = await response.json();
                console.log('Slots received:', data);
                availableSlots.value = data;
            } catch (error) {
                console.error('Error fetching slots:', error);
                availableSlots.value = [];
            } finally {
                loadingSlots.value = false;
            }
        };

        const loadCalendar = async () => {
            loadingCalendar.value = true;
            try {
                const response = await fetch(`${API_BASE_URL}/appointments`);
                if (!response.ok) throw new Error('Failed to fetch appointments');
                const allAppointments = await response.json();
                
                const now = new Date();
                
                // Separate appointments by status and time
                const upcoming = {};
                pastAppointments.value = [];
                cancelledAppointments.value = [];
                
                allAppointments.forEach(apt => {
                    const aptTime = new Date(apt.appointment_time);
                    const dateKey = apt.appointment_time.split('T')[0];
                    
                    if (apt.status === 'cancelled') {
                        cancelledAppointments.value.push(apt);
                    } else if (aptTime < now) {
                        pastAppointments.value.push(apt);
                    } else {
                        if (!upcoming[dateKey]) upcoming[dateKey] = [];
                        upcoming[dateKey].push(apt);
                    }
                });
                
                calendar.value = upcoming;
                pastAppointments.value.sort((a, b) => new Date(b.appointment_time) - new Date(a.appointment_time));
                cancelledAppointments.value.sort((a, b) => new Date(b.appointment_time) - new Date(a.appointment_time));
            } catch (error) {
                console.error('Error fetching calendar:', error);
                calendar.value = {};
                pastAppointments.value = [];
                cancelledAppointments.value = [];
            } finally {
                loadingCalendar.value = false;
            }
        };

        const loadNotifications = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/notifications`);
                if (!response.ok) throw new Error('Failed to fetch notifications');
                const data = await response.json();
                notifications.value = data;
                unreadCount.value = data.filter(n => !n.is_read).length;
            } catch (error) {
                console.error('Error fetching notifications:', error);
            }
        };

        const submitBooking = async () => {
            formError.value = '';
            formSuccess.value = '';

            // Auto-fill name and email from currentUser if logged in
            let clientName = bookingForm.client_name;
            let clientEmail = bookingForm.client_email;
            
            if (isLoggedIn.value && currentUser.value) {
                clientName = currentUser.value.name;
                clientEmail = currentUser.value.email;
            }

            if (!clientName || !clientEmail || !selectedDate.value || !bookingForm.appointment_time) {
                formError.value = 'Please fill in all required fields';
                return;
            }

            bookingLoading.value = true;
            try {
                const response = await fetch(`${API_BASE_URL}/appointments`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        client_name: clientName,
                        client_email: clientEmail,
                        client_phone: bookingForm.client_phone,
                        appointment_date: selectedDate.value,
                        appointment_time: bookingForm.appointment_time,
                        notes: bookingForm.notes
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to book appointment');
                }

                formSuccess.value = '✅ Consultation booked successfully! Check your email for confirmation.';
                bookingForm.client_name = '';
                bookingForm.client_email = '';
                bookingForm.client_phone = '';
                bookingForm.appointment_time = '';
                bookingForm.notes = '';
                selectedDate.value = '';
                availableSlots.value = [];

                await loadCalendar();
                await loadNotifications();
                if (isLoggedIn.value) {
                    await loadUserAppointments();
                }
            } catch (error) {
                formError.value = error.message || 'Failed to book appointment';
            } finally {
                bookingLoading.value = false;
            }
        };

        const connectWebSocket = () => {
            try {
                ws = new WebSocket(WS_URL);
                ws.onopen = () => console.log('WebSocket connected');
                ws.onmessage = (event) => {
                    const notification = JSON.parse(event.data);
                    notifications.value.unshift(notification);
                    unreadCount.value += 1;
                    loadCalendar();
                };
                ws.onerror = (error) => console.error('WebSocket error:', error);
                ws.onclose = () => {
                    console.log('WebSocket disconnected');
                    setTimeout(connectWebSocket, 3000);
                };
            } catch (error) {
                console.error('Failed to connect WebSocket:', error);
            }
        };

        onMounted(() => {
            minDate.value = getMinDate();
            loadCalendar();
            loadNotifications();
            connectWebSocket();
            
            // Show admin login modal if admin route is accessed
            if (adminRoute === 'true') {
                showAdminLogin.value = true;
            }
        });

        onUnmounted(() => {
            if (ws) ws.close();
        });

        const checkAdminPassword = () => {
            adminError.value = '';
            console.log('Admin password entered:', adminPassword.value);
            console.log('Expected password:', ADMIN_PASSWORD);
            if (adminPassword.value === ADMIN_PASSWORD) {
                console.log('Password correct! Logging in...');
                isAdmin.value = true;
                showAdminLogin.value = false;
                adminPassword.value = '';
                activeTab.value = 'calendar';
            } else {
                console.log('Password incorrect');
                adminError.value = 'Invalid password';
                adminPassword.value = '';
            }
        };

        const logoutAdmin = () => {
            isAdmin.value = false;
            activeTab.value = 'booking';
            showCancelModal.value = false;
            selectedAppointment.value = null;
            cancellationMessage.value = '';
            // Redirect to home page
            window.location.href = 'http://localhost:8000';
        };

        const openCancelModal = (appointment) => {
            selectedAppointment.value = appointment;
            cancellationMessage.value = '';
            cancelError.value = '';
            cancelSuccess.value = '';
            showCancelModal.value = true;
        };

        const cancelAppointment = async () => {
            cancelError.value = '';
            cancelSuccess.value = '';
            
            if (!selectedAppointment.value) return;
            
            try {
                const response = await fetch(`${API_BASE_URL}/appointments/${selectedAppointment.value.id}/cancel`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        cancellation_reason: cancellationMessage.value,
                        client_email: selectedAppointment.value.client_email,
                        client_name: selectedAppointment.value.client_name
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to cancel appointment');
                }

                cancelSuccess.value = 'Appointment cancelled and email sent to client!';
                setTimeout(() => {
                    showCancelModal.value = false;
                    loadCalendar();
                }, 2000);
            } catch (error) {
                cancelError.value = error.message;
            }
        };

        const handleAuth = async () => {
            authError.value = '';
            authSuccess.value = '';

            if (showRegister.value && !authForm.name) {
                authError.value = 'Please enter your name';
                return;
            }
            if (!authForm.email || !authForm.password) {
                authError.value = 'Please fill in all fields';
                return;
            }
            if (showRegister.value && authForm.password !== authForm.confirmPassword) {
                authError.value = 'Passwords do not match';
                return;
            }

            authLoading.value = true;
            try {
                const endpoint = showRegister.value ? '/register' : '/login';
                const response = await fetch(`${API_BASE_URL}/auth${endpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: authForm.name,
                        email: authForm.email,
                        password: authForm.password
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Authentication failed');
                }

                const data = await response.json();
                currentUser.value = data.user;
                isLoggedIn.value = true;
                authSuccess.value = showRegister.value ? 'Account created successfully!' : 'Logged in successfully!';
                authForm.name = '';
                authForm.email = '';
                authForm.password = '';
                authForm.confirmPassword = '';
                showRegister.value = false;
                activeTab.value = 'dashboard';
                loadUserAppointments();
            } catch (error) {
                authError.value = error.message;
            } finally {
                authLoading.value = false;
            }
        };

        const logoutClient = () => {
            isLoggedIn.value = false;
            currentUser.value = null;
            activeTab.value = 'booking';
            upcomingAppointments.value = [];
            appointmentHistory.value = [];
        };

        const loadUserAppointments = async () => {
            if (!currentUser.value) return;
            try {
                const response = await fetch(`${API_BASE_URL}/appointments?email=${currentUser.value.email}`);
                if (!response.ok) throw new Error('Failed to fetch appointments');
                const appointments = await response.json();
                
                const now = new Date();
                upcomingAppointments.value = appointments.filter(apt => 
                    new Date(apt.appointment_time) > now && apt.status !== 'cancelled'
                );
                appointmentHistory.value = appointments.filter(apt => 
                    new Date(apt.appointment_time) <= now || apt.status === 'cancelled'
                ).sort((a, b) => new Date(b.appointment_time) - new Date(a.appointment_time));
            } catch (error) {
                console.error('Error loading appointments:', error);
            }
        };

        const sendPasswordResetEmail = async () => {
            forgotPasswordError.value = '';
            if (!forgotPasswordEmail.value) {
                forgotPasswordError.value = 'Please enter your email';
                return;
            }

            forgotPasswordLoading.value = true;
            try {
                const response = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: forgotPasswordEmail.value })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to send reset email');
                }

                forgotPasswordStep.value = 2;
            } catch (error) {
                forgotPasswordError.value = error.message;
            } finally {
                forgotPasswordLoading.value = false;
            }
        };

        return {
            activeTab,
            showNotifications,
            bookingLoading,
            loadingSlots,
            loadingCalendar,
            formError,
            formSuccess,
            selectedDate,
            minDate,
            availableSlots,
            calendar,
            sortedCalendar,
            notifications,
            unreadCount,
            bookingForm,
            formatDate,
            formatTime,
            formatSlotTime,
            loadAvailableSlots,
            submitBooking,
            isAdmin,
            showAdminLogin,
            adminPassword,
            adminError,
            checkAdminPassword,
            logoutAdmin,
            showCancelModal,
            selectedAppointment,
            cancellationMessage,
            cancelError,
            cancelSuccess,
            openCancelModal,
            cancelAppointment,
            loadCalendar,
            showTermsModal,
            isLoggedIn,
            currentUser,
            showRegister,
            authLoading,
            authError,
            authSuccess,
            authForm,
            handleAuth,
            logoutClient,
            upcomingAppointments,
            appointmentHistory,
            loadUserAppointments,
            showForgotPassword,
            forgotPasswordEmail,
            forgotPasswordError,
            forgotPasswordLoading,
            forgotPasswordStep,
            sendPasswordResetEmail,
            adminCalendarView,
            pastAppointments,
            cancelledAppointments
        };
    }
});

// ============================================================================
// MOUNT APP
// ============================================================================

app.mount('#app');
