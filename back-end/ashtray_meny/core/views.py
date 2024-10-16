from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import User, Shop, Product, Category, Review, Order, WishList


# User CRUD Views
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['email', 'username', 'password']  # Add more fields as needed
    template_name = 'user_form.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['email', 'username', 'password']  # Add more fields as needed
    template_name = 'user_form.html'


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_list')
    template_name = 'user_confirm_delete.html'


# Shop CRUD Views
class ShopListView(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'shop_list.html'
    context_object_name = 'shops'


class ShopDetailView(LoginRequiredMixin, DetailView):
    model = Shop
    template_name = 'shop_detail.html'
    context_object_name = 'shop'


class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    fields = ['shop_name', 'shop_owner', 'category', 'shop_image']  # Add more fields as needed
    template_name = 'shop_form.html'


class ShopUpdateView(LoginRequiredMixin, UpdateView):
    model = Shop
    fields = ['shop_name', 'shop_owner', 'category', 'shop_image']  # Add more fields as needed
    template_name = 'shop_form.html'


class ShopDeleteView(LoginRequiredMixin, DeleteView):
    model = Shop
    success_url = reverse_lazy('shop_list')
    template_name = 'shop_confirm_delete.html'


# Product CRUD Views
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['product_name', 'price', 'shop', 'category']  # Add more fields as needed
    template_name = 'product_form.html'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['product_name', 'price', 'shop', 'category']  # Add more fields as needed
    template_name = 'product_form.html'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = 'product_confirm_delete.html'


# Category CRUD Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description', 'category_image']
    template_name = 'category_form.html'


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description', 'category_image']
    template_name = 'category_form.html'


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'category_confirm_delete.html'


# Review CRUD Views
class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'review_detail.html'
    context_object_name = 'review'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['user', 'product', 'shop', 'rating', 'comment']
    template_name = 'review_form.html'


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['user', 'product', 'shop', 'rating', 'comment']
    template_name = 'review_form.html'


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('review_list')
    template_name = 'review_confirm_delete.html'


# Order CRUD Views
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['user', 'total_amount', 'order_status', 'products']
    template_name = 'order_form.html'


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['user', 'total_amount', 'order_status', 'products']
    template_name = 'order_form.html'


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    template_name = 'order_confirm_delete.html'


# WishList CRUD Views
class WishListView(LoginRequiredMixin, ListView):
    model = WishList
    template_name = 'wishlist_list.html'
    context_object_name = 'wishlists'


class WishListDetailView(LoginRequiredMixin, DetailView):
    model = WishList
    template_name = 'wishlist_detail.html'
    context_object_name = 'wishlist'


class WishListCreateView(LoginRequiredMixin, CreateView):
    model = WishList
    fields = ['user', 'product']
    template_name = 'wishlist_form.html'


class WishListUpdateView(LoginRequiredMixin, UpdateView):
    model = WishList
    fields = ['user', 'product']
    template_name = 'wishlist_form.html'


class WishListDeleteView(LoginRequiredMixin, DeleteView):
    model = WishList
    success_url = reverse_lazy('wishlist_list')
    template_name = 'wishlist_confirm_delete.html'
