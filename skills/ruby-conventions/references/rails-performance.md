# Rails Performance Patterns

## Background Jobs

**Never do expensive work in request cycle:**
```ruby
# Good: Background job
UserMailer.welcome(user).deliver_later
ProcessOrderJob.perform_later(order.id)

# Bad: Synchronous
UserMailer.welcome(user).deliver_now  # Blocks request
```

## Caching

```ruby
# Fragment caching
<% cache @user do %>
  <%= render @user %>
<% end %>

# Low-level caching
def expensive_calculation
  Rails.cache.fetch("calculation:#{id}", expires_in: 1.hour) do
    # expensive work
  end
end

# Russian doll caching
<% cache [@user, @user.posts.maximum(:updated_at)] do %>
  <% @user.posts.each do |post| %>
    <% cache post do %>
      <%= render post %>
    <% end %>
  <% end %>
<% end %>
```

## Query Optimization

```ruby
# Eager loading (prevents N+1)
User.includes(:posts, :comments)

# Select only needed columns
User.select(:id, :email)

# Pluck for simple values
User.pluck(:email)  # Returns array of strings

# Batch processing
User.find_each(batch_size: 1000) do |user|
  process(user)
end
```

## Database Indices

```ruby
# Migration
add_index :users, :email, unique: true
add_index :posts, [:user_id, :created_at]
add_index :orders, :status, where: "status = 'pending'"  # Partial index
```

## Profiling

```ruby
# Gemfile
gem 'rack-mini-profiler'
gem 'memory_profiler'
gem 'bullet'  # N+1 detection

# bullet.rb
Bullet.enable = true
Bullet.alert = true
Bullet.bullet_logger = true
```

## Sidekiq Configuration

```ruby
# config/sidekiq.yml
:concurrency: 10
:queues:
  - [critical, 3]
  - [default, 2]
  - [low, 1]

# Job with retry
class ProcessOrderJob < ApplicationJob
  queue_as :default
  retry_on StandardError, attempts: 3, wait: :exponentially_longer

  def perform(order_id)
    Order.find(order_id).process!
  end
end
```
