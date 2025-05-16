from behave import given, when, then
from django.contrib.auth.models import User
from django.test.client import Client
from website.models import Store, UserExtended
from django.urls import reverse


@given('a user named "{username}" with password "{password}"')
def step_create_user(context, username, password):
    user = User.objects.create_user(username=username, password=password)
    UserExtended.objects.get_or_create(user=user)

    if not hasattr(context, "users"):
        context.users = {}

    context.users[username] = {
        "user": user,
        "password": password
    }


@when('"{username}" logs in')
def step_user_logs_in(context, username):
    user_data = context.users[username]
    client = Client()
    logged_in = client.login(username=username, password=user_data["password"])
    assert logged_in is True
    context.client = client
    context.logged_in_user = user_data["user"]


@when('they create a store named "{store_name}"')
def step_create_store(context, store_name):
    response = context.client.get('/add-new-store/', {'store_name': store_name})
    assert response.status_code == 302  # redirect expected


@then('the store "{store_name}" should exist')
def step_store_should_exist(context, store_name):
    assert Store.objects.filter(name=store_name).exists()


@then('"{username}" should have own_store=True')
def step_user_owns_store(context, username):
    user = User.objects.get(username=username)
    user_ext = UserExtended.objects.get(user=user)
    assert user_ext.own_store is True


@when('"{username}" adds user "{other_username}" to the store "{store_name}"')
def step_add_user_to_store(context, username, other_username, store_name):
    store = Store.objects.get(name=store_name)
    response = context.client.get(reverse('profile_add_user_store'), {
        'store_id': store.id,
        'user_username': other_username
    })
    assert response.status_code == 302


@then('"{username}" should be a member of "{store_name}"')
def step_user_is_member_of_store(context, username, store_name):
    user = User.objects.get(username=username)
    store = Store.objects.get(name=store_name)
    assert user in store.users.all()


@then('"{username}" should have own_store=False')
def step_user_does_not_own_store(context, username):
    user = User.objects.get(username=username)
    user_ext = UserExtended.objects.get(user=user)
    print(user_ext.own_store)
    assert user_ext.own_store is False


@when('"{username}" removes user "{other_username}" from the store "{store_name}"')
def step_remove_user_from_store(context, username, other_username, store_name):
    store = Store.objects.get(name=store_name)
    response = context.client.get(reverse('profile_remove_user_store'), {
        'store_id': store.id,
        'user_username': other_username
    })
    assert response.status_code == 302


@then('"{username}" should not be a member of "{store_name}"')
def step_user_not_in_store(context, username, store_name):
    user = User.objects.get(username=username)
    store = Store.objects.get(name=store_name)
    assert user not in store.users.all()


@when('"{username}" deletes the store "{store_name}"')
def step_user_deletes_store(context, username, store_name):
    store = Store.objects.get(name=store_name)
    response = context.client.get(reverse('profile_remove_store'), {
        'store_id': store.id
    })
    assert response.status_code == 302


@then('the store "{store_name}" should no longer exist')
def step_store_does_not_exist(context, store_name):
    assert not Store.objects.filter(name=store_name).exists()
